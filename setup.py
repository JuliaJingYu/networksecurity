'''
The setup.py file is used to configure the package and its dependencies. 
It specifies the package name, version, author, description, and other metadata. 
It also lists the required dependencies for the package to function properly.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements.txt file and returns a list of dependencies.
    
    Args:
        file_path (str): The path to the requirements.txt file.

    Returns:
        List[str]: A list of dependencies.
    """
    requirement_lst: List[str] = []
    try:
        with open("requirements.txt", 'r') as f:
            # Read the lines from the requirements.txt file, strip whitespace, and filter out empty lines
            lines = f.readlines()
             fi# process each line to remove whitespace and ignore empty lines
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
        return requirement_lst
    except FileNotFoundError:
        print("Error: requirements.txt file not found.")
    return []

print(get_requirements("requirements.txt"))

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Julia Y.",
    author_email="happykingdom.planet@gmail.com",
    description="A package for network security analysis.",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)