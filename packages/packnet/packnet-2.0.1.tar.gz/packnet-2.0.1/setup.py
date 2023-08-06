from setuptools import setup, find_packages



README = open("README.md").read()



setup(  name = "packnet",
        version = "2.0.1",
        description = "Python3 package for low-level networking",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/c0mplh4cks/packnet",
        author = "c0mplh4cks",
        license = "MIT",
        packages = find_packages(),
        python_requires = ">=3",
)
