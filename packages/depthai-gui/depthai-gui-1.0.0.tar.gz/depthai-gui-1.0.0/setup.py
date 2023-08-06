from setuptools import setup, find_packages
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "PyFlow", "Core"))
from version import currentVersion

setup(
    name="depthai-gui",
    version=str(currentVersion()),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['depthai-gui = PyFlow.Scripts:main']
    },
    include_package_data=True,
    author="Luxonis",
    author_email="support@luxonis.com",
    description="DepthAI Pipeline Builder GUI",
    keywords="depthai gui ide pipeline builder node",
    url="https://github.com/luxonis/depthai-gui",   # project home page
    project_urls={
        "Bug Tracker": "https://github.com/luxonis/depthai-gui/issues",
        "Documentation": "https://pyflow.readthedocs.io",
        "Source Code": "https://github.com/luxonis/depthai-gui",
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License'
    ],
    install_requires=[
        "PySide2",
        "Qt.py",
        "blinker",
        "nine",
        "docutils",
        "depthai==0.0.2.1+22ad34c8264fc3a9a919dbc5c01e3ed3eb41f5aa",
        "opencv-python"
    ],
    dependency_links=[
        'https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/depthai'
    ],
)
