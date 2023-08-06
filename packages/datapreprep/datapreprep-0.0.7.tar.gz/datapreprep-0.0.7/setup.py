from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='datapreprep',
  version='0.0.7',
  description='A Data Pre Processing Package',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://share.streamlit.io/mohammed-muzzammil/data_pre_processing/main/st1.py',  
  author='Mohammed Muzzammil',
  author_email='muzzammilsilat56@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='data processing', 
  packages=find_packages(),
  install_requires=['pandas','numpy','sklearn','matplotlib','seaborn','scipy','random'] 
)