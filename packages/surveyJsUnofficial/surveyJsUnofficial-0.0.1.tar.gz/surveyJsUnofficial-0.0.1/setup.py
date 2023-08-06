from setuptools import find_packages, setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
  name='surveyJsUnofficial',
  version='0.0.1',
  description='A basic library to access surveyJs api.',
  #long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pramod Gaikwad',
  #license='MIT', 
  classifiers=classifiers,
  keywords='surveyJs python survey free', 
  packages=find_packages(),
  install_requires=[''] 
)

