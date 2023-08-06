from setuptools import setup, find_packages

__author__ = 'Tiago Barbosa'
__license__ = "BSD"
__email__ = "tiago.l.barbosa@tecnico.ulisboa.pt"

setup(
   name='dgnx',
   version='0.1.2',
   license='BSD-Clause-2',
   author='Tiago Barbosa',
   author_email='tiago.l.barbosa@tecnico.ulisboa.pt',
   url='https://github.com/raitonvortex/dgnx',
   description='Dynamic Graph NetworkX Library',
   install_requires=[
       "pytest",
       "networkx",
       "numpy",
       "scipy",
       "matplotlib"
   ],
         packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test", "dgnx.tests", "dgnx.tests.*"]),

)