from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='getipinfo',
  version='1.0.0',
  description='tool to get ip as well as related info',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Alexandru Dumitru',
  author_email='dumalex222@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ip', 
  packages=find_packages(),
  install_requires=['requests'] 
)