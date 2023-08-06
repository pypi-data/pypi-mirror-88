from typing import Tuple

from moodlerpd.client.request_client import RequestClient
from moodlerpd.state.course import Course
from moodlerpd.state.category import Category


class InfoHandler:
    """
    Fetches and parses the various endpoints in Moodle.
    """

    def __init__(self, request_client: RequestClient):
        self.request_client = request_client
        # oldest supported Moodle version
        self.version = 2011120500

    def fetch_userid_and_version(self) -> Tuple[str, int]:
        """
        Ask the Moodle system for the user id.
        @return: the userid
        """
        result = self.request_client.post('core_webservice_get_site_info')

        if 'userid' not in result:
            raise RuntimeError('Error could not receive your user ID!')

        userid = result.get('userid', '')

        version = result.get('version', '2011120500')

        try:
            version = int(version.split('.')[0])
        except Exception as e:
            raise RuntimeError('Error could not parse version string: "%s" Error: %s' % (version, e))

        return userid, version

    def fetch_courses(self, userid: str) -> [Course]:
        """
        Queries the Moodle system for all courses the user
        is enrolled in.
        @param userid: the user id
        @return: A list of courses
        """
        data = {'userid': userid}

        result = self.request_client.post('core_enrol_get_users_courses', data)

        results = []

        for course in result:
            results.append(Course(course.get('id', 0),
                                  course.get('fullname', ''),
                                  course.get('category', -1)))

        return results

    def fetch_search_coursers(self, criteria_name: str, criteria_value: str) -> [Course]:
        """
       Queries the Moodle system for search courses by criteria.
       @param criteria_name: criteria name (search, modulelist (only admins),
        blocklist (only admins), tagid)
       @param criteria_value: criteria value
       @return: A list of courses
       """
        data = {
            'criterianame': criteria_name,
            'criteriavalue': criteria_value
        }

        result = self.request_client.post('core_course_search_courses', data)

        results = []

        for course in result['courses']:
            results.append(Course(course.get('id', 0),
                                  course.get('fullname', ''),
                                  course.get('categoryid', -1)))

        return results

    def fetch_categories(self) -> [Category]:
        """
        Queries the Moodle system for all categories.
        @return: A list all categories
        """

        categories = self.request_client.post('core_course_get_categories')

        results = []

        for category in categories:
            results.append(Category(category.get('id', 0),
                                    category.get('name', ''),
                                    category.get('parent', -1)))

        return results
