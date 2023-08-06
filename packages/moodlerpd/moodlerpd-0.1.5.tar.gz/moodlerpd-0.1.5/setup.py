from setuptools import setup, find_packages

packages = find_packages()

setup(
    name='moodlerpd',
    version='0.1.5',
    description='moodlerpd that downloads course content fast from moodle',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'moodlerpd = moodlerpd.main:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        'colorama>=0.4.3',
        'readchar>=2.0.1',
        'certifi>=2020.4.5.2',
        'html2text>=2020.1.16',
        'requests>=2.24.0',
        'setuptools~=45.2.0',
        'youtube_dl>=2020.9.20'
    ]
)
