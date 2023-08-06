from setuptools import setup, find_packages

setup(name="boomdiff",
    version='2.0',
    author="Minhaun Li, Oksana Makarova, Timothy Williamson, Kevin Hare",
    description="Optimizes user-specified objective functions of many variables using gradient-based optimization; relies on autodifferentiation for fast computation of gradients.", 
    url="https://github.com/team-boomeraang/cs107-FinalProject",
    packages=find_packages(), 
    install_requires=['numpy',
                      'matplotlib'])
