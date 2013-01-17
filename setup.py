# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='SPL',
    version='0.0.1-dev',
    author='Augusto Roccasalva',
    author_email='augusto@rocctech.com.ar',
    url='http://dev.rocctech.com.ar/projects/spl',
    description='Supplier Management Account',
    download_url='http://dev.rocctech.com.ar/projects/spl/wiki/Downloads',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Office/Bussiness :: Financial :: Accounting',
        'Topic :: Office/Bussiness :: Financial :: Purchasing',
    ],
    platforms='any',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        #'psycopg2',
        #'gunicorn',
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'Flask-Restless',
        #'Flask-Assets',
        #'cssmin',
        #'pyScss',
    ],
    entry_points = """\
    [console_scripts]
    run-spl = spl.commands:main
    """
)
