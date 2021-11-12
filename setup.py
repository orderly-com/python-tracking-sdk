import os
from setuptools import setup, find_packages

setup(
    name='python-tracking-sdk',
    version='1.0.0',
    url='https://github.com/orderly-com/python-tracking-sdk',
    license='BSD',
    description='A sdk for python to store tracking data in orderly cdp.',
    author='RayYang',
    author_email='ray.yang@ezorderly.com',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['setuptools', 'requests'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ]
)