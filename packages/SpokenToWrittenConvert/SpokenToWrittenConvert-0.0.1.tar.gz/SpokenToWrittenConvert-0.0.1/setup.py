
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SpokenToWrittenConvert',
  version='0.0.1',
  description='Spoken english to written english convertor',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='MOHIT CHVK',
  author_email='mohit.chvk@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='convertor', 
  packages=find_packages(),
  python_requires='>=3.6',
  install_requires=["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2","SpeechRecognition>=3"]
)