"""
Flask-easy
-------------

A simple rest extension 
"""
from setuptools import setup

setup(
    name='Flask-easy',
    version='1.0',
    url='',
    license='BSD',
    author='Bruno Agutoli',
    author_email='bruno.agutoli@gmail.com',
    description='A simple rest framework',
    long_description=__doc__,
    py_modules=['flask_easy'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
