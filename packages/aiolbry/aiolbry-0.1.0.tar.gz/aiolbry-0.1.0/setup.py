from setuptools import setup
from generator import generate_lbryd_wrapper
from os import path
from setuptools.command.build_py import build_py
from aiolbry import __version__

NAME = "aiolbry"


class GenerateOnBuild(build_py):
    """ Generates the actual file for release at build time """

    def run(self):
        generate_lbryd_wrapper()
        build_py.run(self)


# To read markdown file
this_directory = path.abspath(path.dirname(__file__))

with open(
    path.join(this_directory, "README.md"), mode="r", encoding="utf-8"
) as outfile:
    long_description = outfile.read()

setup(
    name=NAME,
    url="https://gitlab.com/jamieoglindsey0/aiolbry",
    author="Jamie Lindsey",
    author_email="jamieoglindsey0@gmail.com",
    version=__version__,
    py_modules=[
        NAME,
    ],
    license="MIT License",
    description="An asynchronous binded Python3.7+ API for the LBRYD and LBRYCRD network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=["black", "aiohttp", "aiofiles"],
    python_requires=">=3",
    cmdclass={"build_py": GenerateOnBuild},
)
