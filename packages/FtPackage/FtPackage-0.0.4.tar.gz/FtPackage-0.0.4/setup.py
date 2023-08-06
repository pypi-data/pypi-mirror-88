import pathlib
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

HERE = pathlib.Path(__file__).parent
 
setup(
  name='FtPackage',
  version='0.0.4',
  description='built-in python functions',
  long_description=open(HERE/'README.txt').read() + '\n\n' + open(HERE/'CHANGELOG.txt').read(),
  url='',  
  author='Punya Keerthi',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='built-in', 
  packages=["sam"],
  install_requires=['pandas','numpy'],
  entry_points={
        "console_scripts": [
            "sam=sam.__init__:main",
        ]
    },
)