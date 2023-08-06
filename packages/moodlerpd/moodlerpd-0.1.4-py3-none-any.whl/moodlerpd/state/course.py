from moodlerpd.state.file import File
from moodlerpd.utils.path_tools import PathTools
from moodlerpd.state.category import Category


class Course:
    def __init__(self, _id: int, fullname: str, category_id: int, files: [File] = [], categories: [Category] = []):
        self.id = _id
        self.fullname = fullname
        self.category_id = category_id
        self.files = files
        self.categories = categories

        self.overwrite_name_with = None
        self.create_directory_structure = True

    @staticmethod
    def build_categories(course_category: int, categories: [Category]) -> [Category]:
        """
        Build course tree category by all categories in Moodle
        :param course_category: course category
        :param categories: all categories
        :return: course categories
        """
        course_categories = []

        category = next((category for category
                         in categories if category.id == course_category), None)

        if category:
            course_categories = Course.build_categories(category.parent_id, categories)

        return course_categories + [category] if category else course_categories

    def __str__(self):
        message = 'Course ('
        message += 'id: %s' % self.id
        message += ', fullname: "%s"' % (PathTools.to_valid_name(self.fullname))
        message += ', category_id: "%s"' % self.category_id
        message += ', overwrite_name_with: "%s"' % (PathTools.to_valid_name(self.overwrite_name_with))
        message += ', create_directory_structure: %s' % self.create_directory_structure
        message += ', files: %s' % (len(self.files))
        message += ', categories: %s' % (','.join(str(category.name) for category in self.categories))
        message += ')'
        return message
