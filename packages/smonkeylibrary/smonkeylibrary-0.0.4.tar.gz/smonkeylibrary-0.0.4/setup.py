from setuptools import setup, find_packages
from PIL import Image
import requests
from io import BytesIO

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='smonkeylibrary',
  version='0.0.4',
  description='The smonkey library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mattia Rigiroli',
  author_email='mattiarigiroli@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['requests', 'io'] 
)
