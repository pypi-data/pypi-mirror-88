#!/usr/bin/env python

from setuptools import setup
import versioneer

setup(name='s3fs',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      description='Convenient Filesystem interface over S3',
      url='http://github.com/dask/s3fs/',
      maintainer='Martin Durant',
      maintainer_email='mdurant@continuum.io',
      license='BSD',
      keywords='s3, boto',
      packages=['s3fs'],
      python_requires='>= 3.7',
      install_requires=[open('requirements.txt').read().strip().split('\n')],
      zip_safe=False)
