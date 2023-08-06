
from setuptools import setup, find_packages

setup(
    name='bagua',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='Apache-2.0',
    description='An example python package',
    long_description=open('README.txt').read(),
    install_requires=['numpy'],
    url='https://github.com/NOBLES5E/bagua',
    author='Xiangru Lian',
    author_email='admin@mail.xrlian.com'
)
