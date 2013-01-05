"""`holy` lives on `GitHub <http://github.com/njoh/holy/>`_."""
from distutils.core import setup

setup(
    name = "holy",
    version = "0.0.2",
    author = "Nima Johari",
    author_email = "nimajohari@gmail.com",
    description = "POC Python AST to Ruby script transformer",
    license = "MIT",
    keywords = "py2rb ast ruby POC",
    packages=['holy', 'holy.test'],
    package_dir = {'': 'lib'},
    package_data={'': ['*.yaml']},
    include_package_data=True,
    scripts=["bin/holy"],
    test_suite="holy.test",
    install_requires = ['docopt>=0.5.0', 'PyYAML>=3.10'],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
)
