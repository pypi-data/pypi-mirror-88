from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ValidateConection',
  version='0.0.1',
  description='Pruebas de conexion para Dongle',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ari Bautista',
  author_email='aribautista66@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Validate Conections For Dongle', 
  packages=find_packages(),
  install_requires=['']
)