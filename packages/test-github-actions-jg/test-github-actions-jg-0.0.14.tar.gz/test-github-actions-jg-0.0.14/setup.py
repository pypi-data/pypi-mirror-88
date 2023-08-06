"Setup script for pydadjoke"

import sys
from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def main():
    "Executes setup when this script is at the top-level"
    import pydadjoke as app

    setup(
        name=app.__project__,
        version=app.__version__,
        description=app.__doc__,
        classifiers=app.__classifiers__,
        author=app.__author__,
        author_email=app.__author_email__,
        url=app.__url__,
        license=[
            c.rsplit('::', 1)[1].strip()
            for c in app.__classifiers__
            if c.startswith('License ::')
        ][0],
        keywords=app.__keywords__,
        packages=find_packages(),
        include_package_data=True,
        platforms=app.__platforms__,
        install_requires=["pandas"],
        extras_require=app.__extra_requires__,
    )

if __name__ == '__main__':
    main()
