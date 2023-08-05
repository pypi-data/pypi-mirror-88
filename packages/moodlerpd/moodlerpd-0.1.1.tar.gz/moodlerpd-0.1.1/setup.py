from setuptools import setup, find_packages


def find_requirements():
    requirements_list = []

    with open('requirements.txt') as requirements_file:
        for install in requirements_file:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages()
requirements = find_requirements()

setup(
    name='moodlerpd',
    version='0.1.1',
    description='moodlerpd that downloads course content fast from moodle',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'moodlerpd = moodlerpd.main:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=requirements,
    zip_safe=False
)
