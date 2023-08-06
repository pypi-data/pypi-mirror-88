

# Group #19

[![Build Status](https://travis-ci.org/team-boomeraang/cs107-FinalProject.svg?branch=master)](https://travis-ci.org/team-boomeraang/cs107-FinalProject)  [![codecov](https://codecov.io/gh/team-boomeraang/cs107-FinalProject/branch/master/graph/badge.svg)](https://codecov.io/gh/team-boomeraang/cs107-FinalProject)

### Team members
* Oksana Makarova
* Minhuan Li
* Timothy Williamson
* Kevin Hare

#### Broader Impact Statement
This AD package has a function of usability that is user-friendly, allowing groups with little to moderate experience to operate this library with ease, thanks to the extensive documentation. The simplicity in defining variables and their derivatives allows the methods and functions of autodiff to differentiate both complex functions and basic functions alike.
With this automatic differentiation package, one can easily ascertain both the value and derivatives of a given function. What makes our library impactful is the ability to easily create one’s own functions inheriting instances of variables using the AD library.
To make contributions to this library, users must import AD from *boomdiff.autodiff*, then create a closure inheriting a variable defined with the AD library. This lessens the inclusivity as a moderate level of skill in Python is required to accomplish this. However, it allows for nearly endless functions to be created for user-specific uses. One example of this use is creating a user-supplied loss function for broad ethical Machine Learning projects. Due to the ability to create user-specific functions, the range of this package’s inclusivity is far wider than that of other packages. The greatest impact would potentially occur with groups seeking an easy way to create their own methods and functions making use of automatic differentiation, as this package is specifically user-friendly in that area compared to others of its kind. While it may not be as efficient or as specialized as other libraries, this ability to create new methods allows this library to have a more widespread range of use than others of its kind and ensures that the process is fair and welcoming to nearly all groups with experience in Python.

## Installation of boomdiff
Below are instructions for the download and installation of the *boomdiff* package. The instructions below are all designed to be run on a command-line interface (Windows, macOS, Linux). Please note that steps (2) and (3) assume that the user has installed [Python](https://www.python.org/). If the user has not installed Python, please see instructions [below](#installation_py)

**Method #1: Installation via PyPi**
Note: this is the preferred method for installing the most up-to-date release of *boomdiff*.
1. In a command-line interface, run the following command:

`pip install boomdiff`

**Method #2: Installation via GitHub**
If installation via PyPi is insufficient, we have provided the instructions below, desgined to download and install the development version of *boomdiff*, available through our GitHub repository.
1. **Download package**:

    The boomdiff package is available at the GitHub address (https://github.com/team-boomeraang/cs107-FinalProject). To download, navigate on the command line to the desired installation location and run:

    `git clone https://github.com/team-boomeraang/cs107-FinalProject.git`

2. **Installation of dependencies**:

    There are two ways to install dependencies, depending on the package manager used. If using `pip`, then run:

    `pip install -r requirements.txt`

    Else, if using Conda or Miniconda for package management, run:

    `conda install --file requirements.txt`

    Finally, if the desired use is to use `pip` to install the package through Conda or Miniconda, run the following sequence of commands:

    `conda install pip`

    `which pip`

    Ensure that the directory of pip to be used falls below 'anaconda' or 'miniconda' in the directory structure.

    `pip install -r requirements.txt`

3. **Set-up and install packages**:

    Next, the `setup.py` file must be run to install boomdiff [boomdiff_optimizer not currently available, see Future Features section below]. Navigate to the newly cloned directory and run:

    `python setup.py install`



<a id='installation_py'></a>

#### Installation of Python
We recommend two possible methods for installation of Python.


1. [Anaconda](https://www.anaconda.com/products/individual) is a package manager that can install Python as well as a variety of common packages (e.g. NumPy, Pandas, scipy). If installed with Anaconda, the instructions below describing `conda install` will be most relevant.


2. Python can also be installed directly (see [here](https://www.python.org/downloads/)). This installation mode will require use of an outside text editor, but may offer more flexibility for installation. If installed via the Python documentation directly, please follow instructions for `pip`.
