import html
from youtube_dl.utils import sanitize_filename
from pathlib import Path


class PathTools:
    """A set of methodes to create correct paths."""

    restricted_filenames = False
    code = 'utf-8'

    @staticmethod
    def to_valid_name(name: str) -> str:
        """Filtering invalide characters in filenames and paths.
        Args:
            name (str): The string that will go through the filtering
        Returns:
            str: The filtered string, that can be used as a filename.
        """

        if name is None:
            return None

        # Moodle saves the title of a section in HTML-Format,
        # so we need to unescape the string
        name = html.unescape(name)

        name = name.replace('\n', ' ')
        name = name.replace('\r', ' ')
        name = name.replace('\t', ' ')
        while '  ' in name:
            name = name.replace('  ', ' ')
        name = sanitize_filename(name, PathTools.restricted_filenames)
        name = name.strip('. ')
        name = name.strip()

        encode_name = name.encode('utf-8', 'ignore')

        if len(encode_name) > 220:
            name = encode_name[:220].decode('utf-8', 'ignore')

        return name

    @staticmethod
    def path_of_file_in_module(
            storage_path: str, course_fullname: str, file_section_name: str, file_module_name: str, file_path: str
    ):
        """
        @param storage_path: The path where all files should be stored.
        @param course_fullname: The name of the course where the file is
                                located.
        @param file_section_name: The name of the section where the file
                                  is located.
        @param file_module_name: The name of the module where the file
                                 is located.
        @param file_path: The additional path of a file (subdirectory).
        @return: A path where the file should be saved.
        """
        path = str(
            Path(storage_path)
            / PathTools.to_valid_name(course_fullname)
            / PathTools.to_valid_name(file_section_name)
            / PathTools.to_valid_name(file_module_name)
            / file_path.strip('/')
        )
        return path

    @staticmethod
    def path_of_category(storage_path: str, category_path: [str]) -> str:
        """
        @param storage_path: The path where all files should be stored.
        @param storage_path: The name of the course where the file is
                                located.
        @param category_path: The name of the section where the file
                                  is located.
        @return: A path where the file should be saved.
        """
        path = str(
            Path(storage_path) /
            '/'.join(PathTools.to_valid_name(category) for category in category_path)
        )
        return path

    @staticmethod
    def path_of_file(storage_path: str, course_fullname: str, file_section_name: str, file_path: str):
        """
        @param storage_path: The path where all files should be stored.
        @param course_fullname: The name of the course where the file is
                                located.
        @param file_section_name: The name of the section where the file
                                  is located.
        @param file_path: The additional path of a file (subdirectory).
        @return: A path where the file should be saved.
        """
        path = str(
            Path(storage_path)
            / PathTools.to_valid_name(course_fullname)
            / PathTools.to_valid_name(file_section_name)
            / file_path.strip('/')
        )
        return path

    @staticmethod
    def flat_path_of_file(storage_path: str, course_fullname: str, file_path: str):
        """
        @param storage_path: The path where all files should be stored.
        @param course_fullname: The name of the course where the file is
                                located.
        @param file_path: The additional path of a file (subdirectory).
        @return: A path where the file should be saved.
        """
        path = str(Path(storage_path) / PathTools.to_valid_name(course_fullname) / file_path.strip('/'))
        return path
