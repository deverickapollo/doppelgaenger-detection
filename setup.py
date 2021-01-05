"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

import subprocess
import pathlib
# Always prefer setuptools over distutils
from setuptools import setup
from setuptools.command.install import install
from subprocess import check_call

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()

#UPDATE WHEN TIME
class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        check_call("python3 -m pip install --upgrade pip".split())
        check_call("brew reinstall hunspell".split())
        check_call("python3 -m pip install cyhunspell wheel pandas language_tool_python spacy scrapy itemadapter wheel numpy Twisted flask timeloop pytz nltk coverage scikit-learn".split())
        subprocess_cmd("python3 -m spacy download de_core_news_sm && python3 -m spacy download en_core_web_sm && python3 -m spacy download fr_core_news_sm && python3 -m spacy download es_core_news_sm")
        subprocess_cmd("python3 -m nltk.downloader punkt && python3 -m nltk.downloader stopwords && python3 -m nltk.downloader averaged_perceptron_tagger")
        install.run(self)



# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(

    # $ pip install doppel-detect
    #
    # And where it will live on PyPI: https://pypi.org/project/doppel-detect
    name='DoppelDetect',  # Required

    version='1.0.0',  # Required

    description='Web Crawler scans the index/main page of the news website The Guardian for articles. \
                In particular, the piece of code retrieves detailed statistics/information about news articles, e.g., \
                title of the article, valid Uniform Resource Locators (URLs) of the article, author of the article, date of appearance, etc.',  # Optional

    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)


    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/hashes4merkle/doppelgaenger-detection',  # Optional

    author='Deverick Simpson and Leon Wolter',  # Optional

    author_email='deverick@apollolabs.io',  # Optional


    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicates who the project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        #These classifiers are *not* checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    # Note that this is a list of additional keywords, separated
    # by commas, to be used to assist searching for the distribution in a
    # larger catalog.
    keywords='sentiment analysis, doppelgänger, doppelgaenger',  # Optional

    # When source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    # package_dir={'': 'src'},  # Optional

    # Specify package directories manually here if your project is
    # simple. Or use find_packages().
    # packages=find_packages(where='src'),  # Required

    # Specify which Python versions to support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5, <4',

    # This field lists other packages that the project depends on to run.
    # Any package put here will be installed by pip when the project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
    cmdclass={
        'install': PreInstallCommand,
    },
)
