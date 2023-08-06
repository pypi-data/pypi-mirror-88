from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert_file("README.md", "rst")
except:
    print ("Warning: pypandoc module not found, could not convert Markdown to reStructuredText." )
    long_description = ""


setup(
    name='pymadx',
    version='1.8.1',
    packages=find_packages(exclude=["docs", "tests", "obsolete"]),
    # Not sure how strict these need to be...
    install_requires=["six>1.0",
                      "future",
                      "matplotlib>=1.7.1",
                      "numpy >= 1.4",
                      "pytransport"],
    # Some version of python2.7
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    python_requires=">=2.7.*",

    author='JAI@RHUL',
    author_email='laurie.nevay@rhul.ac.uk',
    description="Write MADX models and load MADX output.",
    long_description=long_description,
    url='https://bitbucket.org/jairhul/pymadx/',
    license='GPL3',
    keywords='madx accelerator twiss ptc',
)
