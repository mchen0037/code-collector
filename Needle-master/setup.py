from setuptools import setup

setup(
    name='Needle',
    version='1.0.0',
    packages=['needle'],
    install_requires=['flask>=1.0.2','flask-bootstrap','flask-wtf','flask-codemirror'],
    license='MIT',
    long_description=open('README.md').read(),
    author='Denis Vashchenko'
)

