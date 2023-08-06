from setuptools import setup, find_packages
import os


# region[Constants]
GID_LOGGER_AUTHOR = ['Giddius']
GID_LOGGER_SHORT_DESCRIPTION = 'WiP'
GID_LOGGER_LONG_DESCRIPTION_FILE = 'README.md'
GID_LOGGER_VERSION = "0.1.2"
GID_LOGGER_LICENSE = 'MIT'
GID_LOGGER_ENTRY_POINTS = {}
GID_LOGGER_URL = ''
GID_LOGGER_REQUIREMENTS_FILE = 'requirements.txt'
# endregion[Constants]


def get_dependencies():
    # sourcery skip: inline-immediately-returned-variable, list-comprehension
    _out = []
    if os.path.isfile(GID_LOGGER_REQUIREMENTS_FILE) is True:
        with open(GID_LOGGER_REQUIREMENTS_FILE, 'r', errors='replace') as fileobject:
            _temp_list = fileobject.read().splitlines()

        for line in _temp_list:
            if line != '' and line.startswith('#') is False:
                _out.append(line)
    return _out


def get_long_description_type():
    _type_dict = {
        'md': 'text/markdown',
        'rst': 'text/x-rst',
        'txt': 'text/plain'
    }
    _ext = GID_LOGGER_LONG_DESCRIPTION_FILE.split('.')[-1]
    return _type_dict.get(_ext, 'text/plain')


def get_version():
    return GID_LOGGER_VERSION


def get_short_description():
    return GID_LOGGER_SHORT_DESCRIPTION


def get_long_description():
    with open(GID_LOGGER_LONG_DESCRIPTION_FILE, 'r', errors='replace') as fileobject:
        _out = fileobject.read()
    return _out


def get_url():
    return GID_LOGGER_URL


def get_author():
    return GID_LOGGER_AUTHOR


def get_license():
    return GID_LOGGER_LICENSE


def get_entry_points():
    return GID_LOGGER_ENTRY_POINTS


setup(name='gidlogger',
      version=get_version(),
      description=get_short_description(),
      long_description=get_long_description(),
      long_description_content_type=get_long_description_type(),
      url=get_url(),
      author=get_author(),
      license=get_license(),
      packages=find_packages(),
      install_requires=get_dependencies(),
      include_package_data=True,
      entry_points=get_entry_points(),
      options={"bdist_wheel": {"universal": True}}
      )
