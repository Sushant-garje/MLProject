from setuptools import setup,find_packages
from typing import List
HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str)->List[str]:
    '''
    this function ill return a list of requirements from a requirements file
    '''
    requirements = []
    with open(file_path,"r") as file_obj:
        requirements = file_obj.readlines()
        requirements =[req.strip() for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name="mlproject",
    version="0.0.1",
    packages=find_packages(),
    author="Sushant Garje",
    author_email="iamsushantgarje@gmail.com",
    install_requires=get_requirements("requirements.txt"),
    python_requires=">=3.6",

)