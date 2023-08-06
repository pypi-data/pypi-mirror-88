import shutil
import logging

from pathlib import Path

from moodlerpd.config.config_service import ConfigService
from moodlerpd.state.state_service import StateService
from moodlerpd.state.course import Course
from moodlerpd.client.request_client import RequestRejectedError
from moodlerpd.client.request_client import RequestClient
from moodlerpd.client.results_handler import ResultsHandler
from moodlerpd.client.info_handler import InfoHandler


class ClientService:
    def __init__(
            self,
            config_service: ConfigService,
            storage_path: str,
            skip_cert_verify: bool = False,
            log_responses: bool = False,
    ):
        self.config_service = config_service
        self.storage_path = storage_path
        self.recorder = StateService(Path(storage_path) / 'moodlerpd_state.db')
        self.skip_cert_verify = skip_cert_verify

        self.log_responses_to = None
        if log_responses:
            self.log_responses_to = str(Path(storage_path) / 'moodlerpd_responses.log')

    def fetch_state(self) -> [Course]:
        """
        Gets the current status of the configured Moodle account and compares
        it with the last known status for changes. It does not change the
        known state, nor does it download the files.
        @return: List with detected changes
        """
        logging.debug('Fetching current Moodle State...')

        token = self.config_service.get_token()
        moodle_domain = self.config_service.get_moodle_domain()
        moodle_path = self.config_service.get_moodle_path()

        request_client = RequestClient(
            moodle_domain, moodle_path, token, self.skip_cert_verify, self.log_responses_to)

        info_handler = InfoHandler(request_client)

        results_handler = ResultsHandler(request_client, moodle_domain, moodle_path)

        download_course_ids = self.config_service.get_download_course_ids()

        dont_download_course_ids = self.config_service.get_dont_download_course_ids()

        download_category_path = self.config_service.get_download_category_path()

        check_course_category = self.config_service.get_check_course_category()

        criteria_enabled = self.config_service.get_criteria_enabled()

        filtered_courses = []

        try:

            print('\rDownloading account information\033[K', end='')

            userid, version = info_handler.fetch_userid_and_version()
            results_handler.set_version(version)

            categories_list = info_handler.fetch_categories()

            self.recorder.update_categories(categories_list)

            if criteria_enabled:

                criteria_name = self.config_service.get_criteria_name()
                criteria_value = self.config_service.get_criteria_value()

                courses_list = info_handler.fetch_search_coursers(
                    criteria_name, criteria_value)

            else:
                courses_list = info_handler.fetch_courses(userid)

            courses = []
            # Filter unselected courses
            for course in courses_list:
                if ResultsHandler.should_download_course(course, check_course_category,
                                                         download_course_ids, dont_download_course_ids):
                    courses.append(course)

            index = 0
            for course in courses:
                index += 1

                # to limit the output to one line
                limits = shutil.get_terminal_size()

                shorted_course_name = course.fullname
                if len(course.fullname) > 17:
                    shorted_course_name = course.fullname[:15] + '..'

                if download_category_path:
                    course.categories = course.build_categories(course.category_id, categories_list)

                into = '\rDownloading course: '

                status_message = into + ' %3d/%3d [%-17s|%3d|%6s]' % (index, len(courses), shorted_course_name,
                                                                      len(course.categories), course.id)

                if len(status_message) > limits.columns:
                    status_message = status_message[0: limits.columns]

                print(status_message + '\033[K', end='')
                course.files = results_handler.fetch_files(course.id)

                filtered_courses.append(course)

        except (RequestRejectedError, ValueError, RuntimeError) as error:
            raise RuntimeError('Error while communicating with the Moodle System! (%s)' % error)

        logging.debug('Checking for changes...')
        changes = self.recorder.changes_of_new_version(filtered_courses)

        # Filter changes
        changes = self.filter_courses(changes, self.config_service)

        return changes

    @staticmethod
    def filter_courses(changes: [Course], config_service: ConfigService) -> [Course]:
        """
        Filters the changes course list from courses that
        should not get downloaded
        """

        download_course_ids = config_service.get_download_course_ids()
        dont_download_course_ids = config_service.get_dont_download_course_ids()
        download_links_in_descriptions = config_service.get_download_links_in_descriptions()
        download_descriptions = config_service.get_download_descriptions()
        check_course_category = config_service.get_check_course_category()

        filtered_changes = []

        for course in changes:

            if not download_descriptions:
                course_files = []
                for file in course.files:
                    if file.content_type != 'description':
                        course_files.append(file)
                course.files = course_files

            course_files = []
            for file in course.files:
                if not file.content_type == 'description-url':
                    course_files.append(file)

                elif download_links_in_descriptions:
                    add_description_url = True
                    for test_file in course.files:
                        if file.content_fileurl == test_file.content_fileurl:
                            if test_file.content_type != 'description-url':
                                # If a URL in a description also exists as a real link in the course,
                                # then ignore this URL
                                add_description_url = False
                                break
                            elif file.module_id > test_file.module_id:
                                # Always use the link from the older description.
                                add_description_url = False
                                break

                    if add_description_url:
                        course_files.append(file)

            course.files = course_files

            if (ResultsHandler.should_download_course(
                    course, check_course_category, download_course_ids, dont_download_course_ids) and
                    len(course.files) > 0):
                filtered_changes.append(course)

        return filtered_changes
