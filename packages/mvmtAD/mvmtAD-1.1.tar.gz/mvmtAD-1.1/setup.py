from setuptools import setup, find_packages

setup(name='mvmtAD',
    packages=find_packages(),
    version='1.1',
    description='Forward mode automatic differentiation package.',
    url='https://github.com/MVMT107/cs107-FinalProject',
    author='Victoria DiTomasso, Martha Obasi, Matt Egan, Thomas Shay Hill',
    install_requires=['numpy','scipy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest','pytest-cov','unittest'])
