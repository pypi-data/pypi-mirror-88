from dotenv import load_dotenv
import os
from gidtools.gidfiles import writeit, pathmaker

load_dotenv()


WORKSPACEDIR = os.getenv('WORKSPACEDIR')


def produce_inits():
    for dirname, folderlist, filelist in os.walk(pathmaker(WORKSPACEDIR, 'Antipetros_Discord_Bot')):
        if '__init__.py' not in filelist:
            writeit(pathmaker(dirname, '__init__.py'), '')


if __name__ == '__main__':
    produce_inits()
