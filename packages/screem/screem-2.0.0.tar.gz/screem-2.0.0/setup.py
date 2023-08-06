from setuptools import setup, find_packages



README = open("README.md").read()



setup(  name = "screem",
        version = "2.0.0",
        description = "Python3 package for creating graphical user interfaces inside a terminal ",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/c0mplh4cks/screem",
        author = "c0mplh4cks",
        license = "MIT",
        packages = find_packages(),
        python_requires = ">=3",
)
