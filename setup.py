## setup.py is a python file, the presence of which is an indication that the module/package you are about to install has likely been packaged and distributed with Distutils, which is the standard for distributing Python Modules.

import setuptools  ## to setup all the tools

from typing import List  ## importing List



with open("README.md", "r", encoding="utf-8") as f:   ## it will read all the discription from readme file
    long_description = f.read()

__version__ = "0.0.0"      ## version we need to give to it

REPO_NAME = "aps-fault-detection"   ## git repository name
AUTHOR_USER_NAME = "deveshpatil619"          ## git author name
SRC_REPO = "sensor"                     ## project name
AUTHOR_EMAIL = "deveshpatil619@gmail.com"       ## email


REQUIREMENT_FILE_NAME="requirements.txt" ## requirements file
HYPHEN_E_DOT = "-e ."   


def get_requirements()->List[str]:  ## return list that will contain the string values
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list



setuptools.setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for CNN app",
    long_description=long_description,  ## It will come from the readme file
    #long_description_content="text/markdown", ## type of it
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    python_requires = ">=3.7",     ## Minimum Version of python required
     package_dir={"": "sensor"},   ## in sensor folder we need to find the packages
    packages=setuptools.find_packages(where="sensor"),

    install_requires = get_requirements(),

  
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },

   
)






















