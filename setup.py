from imp import load_source
from os.path import join, dirname, abspath
from setuptools import setup, find_packages

lanyon_mod = load_source('lanyon', join(dirname(abspath(__file__)),
                                        'src', 'lanyon', '__init__.py'))

setup(
    name = 'lanyon',
    version = lanyon_mod.__version__,
    url = lanyon_mod.__url__,
    license = 'BSD',
    description = 'Static Site Generator',
    author = 'Arthur Koziel',

    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data={'lanyon': ['templates/default.html'],},
    zip_safe = False,

    test_suite = 'nose.collector',

    # install the lanyon executable
    entry_points = {
        'console_scripts': [
            'lanyon = lanyon.app:main'
        ]
    },
    install_requires = [
        'Jinja2',
    ],
)

