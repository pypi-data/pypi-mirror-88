from setuptools import setup, find_packages

setup(
    name='menupkg',
    version='0.1',
    packages=find_packages(), 
    license='MIT',
    description='A test python package',
    install_requires = ['tabulate'],                      
    url='https://github.com/ubco-mds-2020-labs/data-533-lab-4-monajmn',
    author='F. Liu, M. Jia',
    author_email='liufengcheng_barry@outlook.com'
)

