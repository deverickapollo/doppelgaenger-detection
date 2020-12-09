"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

import os
import atexit
import pathlib
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.install import install


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

def _post_install():
    print('============== POST INSTALL ==============')

    version = "python3 --version" #command to be executed
    spacyPackage = "git clone https://github.com/hashes4merkle/spacy_hunspell.git && git clone https://github.com/hashes4merkle/pyhunspell.git"
    brew = "brew reinstall hunspell"
    numpy = "pip3 install numpy"
    link = "ln -s /usr/local/lib/libhunspell-1.7.a /usr/local/lib/libhunspell.a"
    link2 = "ln -s /usr/local/Cellar/hunspell/1.7.0_2/lib/libhunspell-1.7.dylib /usr/local/Cellar/hunspell/1.7.0_2/lib/libhunspell-1.7.dylib"
    pip = "CFLAGS=$(pkg-config --cflags hunspell) LDFLAGS=$(pkg-config --libs hunspell) pip3 install hunspell"

    # hunspell_include = "export C_INCLUDE_PATH=/usr/local/include/hunspell "
    install_hunspell = "cd spacy_hunspell && pip3 install -r requirements.txt && python3 setup.py install"
    gohome = f"cd {here}"
    install_pyhunspell = "cd pyhunspell && python3 setup.py install"
    download = "python3 -m spacy download de_core_news_sm && python3 -m spacy download en_core_web_sm && python3 -m spacy download fr_core_news_sm && python3 -m spacy download es_core_news_sm"
    nltk = "python3 -m nltk.downloader punkt && python3 -m nltk.downloader stopwords && python3 -m nltk.downloader averaged_perceptron_tagger"
    res = os.system(version)
    print("Returned Value: ", res)
    print(here)
    os.system(spacyPackage)
    os.system(brew)
    os.system(numpy)
    os.system(link)
    os.system(link2)
    os.system(pip)
    os.system(gohome)
#   os.system(hunspell_include)
    os.system(install_hunspell)
    os.system(download)
    os.system(gohome)
    os.system(install_pyhunspell)
    os.system(nltk)


    
    print('========== END OF POST INSTALL ===========')


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


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
    install_requires=['wheel', 'cyhunspell' ,'scrapy','numpy', 'Twisted','flask', 'timeloop','pytz','nltk','language_tool_python','spacy'],  # Optional

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
    cmdclass={'install': new_install},
)
