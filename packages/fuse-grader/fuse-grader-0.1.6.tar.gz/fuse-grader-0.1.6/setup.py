from setuptools import find_packages, setup

__version__ = "0.1.6"


def read_file(name):
    with open(name) as fd:
        return fd.read()


setup(
    name="fuse-grader",
    version=__version__,
    author="Anish Shrestha",
    author_email="anishshrestha@fusemachines.com",
    description="Assignment grader.",
    long_description=read_file("README.md"),
    packages=find_packages(exclude=["tests"]),
    install_requires=read_file("requirements.txt").splitlines(),
)
