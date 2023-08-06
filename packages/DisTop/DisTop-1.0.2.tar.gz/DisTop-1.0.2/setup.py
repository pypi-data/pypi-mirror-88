from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='DisTop',
  version='1.0.2',
  description='Very easy to use https://distop.xyz Stats updater',
  long_description_content_type="text/markdown",
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='MrStretch',
  author_email='markustraus@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='distop, botlist, discord bots,bots', 
  packages=find_packages(),
  install_requires=['aiohttp']
)
