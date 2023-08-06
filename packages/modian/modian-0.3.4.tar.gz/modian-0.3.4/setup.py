
from setuptools import setup, find_packages

NAME = "modian"

setup(name=NAME,
    version='0.3.4',
    author = "Loïc Paulevé",
    author_email = "loic.pauleve@labri.fr",
    description = "Simple python library for Boolean networks",
    long_description = "For teaching purpose",
    install_requires = [
        "jupyter",
        "notebook",
        "pydotplus"
    ],
    py_modules = ["modian_setup"],
    license="CeCILL",
    packages = [NAME],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="boolean networks, model checing, teaching",
)

