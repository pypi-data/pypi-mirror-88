import json

from pathlib import Path


class ConfigService:
    """
    Handles the saving, formatting and loading of the local configuration.
    """

    def __init__(self, storage_path: str):
        self._whole_config = {}
        self.storage_path = storage_path
        self.config_path = str(Path(storage_path) / 'config.json')

    def load(self):
        """
        Opens the configuration file and parse it to a JSON object
        """
        try:
            with open(self.config_path, 'r') as config_file:
                config_raw = config_file.read()
                self._whole_config = json.loads(config_raw)
        except IOError:
            raise ValueError('No config found!')

    def get_property(self, key: str) -> any:
        """
        Returns a property if configured
        """
        try:
            return self._whole_config[key]
        except KeyError:
            raise ValueError('The "$s" property is not yet configured!', key)

    def set_property(self, key: str, value: any):
        """
        Sets a property in the JSON object
        """
        self._whole_config.update({key: value})
        self.save()

    def remove_property(self, key: str):
        """
        Remove a property from the JSON
        """
        self._whole_config.pop(key, None)
        self.save()

    def save(self):
        """
        Saves the JSON object back to file
        """
        with open(self.config_path, 'w+', encoding='utf-8') as config_file:
            config_formatted = json.dumps(self._whole_config, indent=4)
            config_file.write(config_formatted)

    def get_token(self) -> str:
        """
        returns a stored token
        """
        try:
            return self.get_property('token')
        except ValueError:
            raise ValueError('Not yet configured!')

    def get_moodle_domain(self) -> str:
        """
        returns a stored moodle_domain
        """
        try:
            return self.get_property('moodle_domain')
        except ValueError:
            raise ValueError('Not yet configured!')

    def get_moodle_path(self) -> str:
        # returns a stored moodle_path
        try:
            return self.get_property('moodle_path')
        except ValueError:
            raise ValueError('Not yet configured!')

    def get_dont_download_course_ids(self) -> []:
        # returns a stored list of ids that should not be downloaded
        try:
            return self.get_property('dont_download_course_ids')
        except ValueError:
            return []

    def get_download_linked_files(self) -> bool:
        # returns if linked files should be downloaded
        try:
            return self.get_property('download_linked_files')
        except ValueError:
            return True

    def get_download_course_ids(self) -> []:
        # returns a stored list of course ids hat should be downloaded
        try:
            return self.get_property('download_course_ids')
        except ValueError:
            return []

    def get_download_links_in_descriptions(self) -> bool:
        # returns a stored boolean if links in descriptions should be downloaded
        try:
            return self.get_property('download_links_in_descriptions')
        except ValueError:
            return False

    def get_download_descriptions(self) -> bool:
        # returns a stored boolean if descriptions should be downloaded
        try:
            return self.get_property('download_descriptions')
        except ValueError:
            return True

    def get_criteria_enabled(self) -> bool:
        # return search course criteria enabled
        try:
            return self.get_property('criteria_enabled')
        except ValueError:
            return False

    def get_criteria_name(self) -> str:
        # return search course criteria name
        try:
            return self.get_property('criteria_name')
        except ValueError:
            raise ValueError('Not yet configured!')

    def get_criteria_value(self) -> str:
        # return search course criteria name
        try:
            return self.get_property('criteria_value')
        except ValueError:
            raise ValueError('Not yet configured!')

    def get_restricted_filenames(self) -> bool:
        # returns the filenames should be restricted
        try:
            return self.get_property('restricted_filenames')
        except ValueError:
            return False

    def get_download_category_path(self) -> bool:
        # returns a stored boolean if category should be downloaded
        try:
            return self.get_property('download_category_path')
        except ValueError:
            return True

    def get_check_course_category(self) -> bool:
        # returns a stored boolean if category should be downloaded
        try:
            return self.get_property('check_course_category')
        except ValueError:
            return True
