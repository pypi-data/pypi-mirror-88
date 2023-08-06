from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fakelibraries',
  version='0.0.1',
  description='A basic fake data probvider for health care system',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Health Data Research UK',
  author_email='kabir.khan@hdruk.ac.uk',
  license='MIT', 
  classifiers=classifiers,
  keywords='fakedataprovider', 
  packages=find_packages(),
  install_requires=['random'] 
)