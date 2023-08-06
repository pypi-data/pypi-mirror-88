from setuptools import setup

setup(
   name='imlp',
   version='1.0.1',
   description='IMLP SDK',
   author='bruce',
   author_email='zhaozhenxiu@inspur.com',
   packages=['imlp'],  #same as name
   install_requires=['pandas', 'scikit-learn', 'pymysql', 'pathlib2', 'minio']
)
