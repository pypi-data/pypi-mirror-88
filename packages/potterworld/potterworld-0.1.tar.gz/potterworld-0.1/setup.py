from setuptools import setup, find_packages
setup( 
    name='potterworld', 
    version='0.1', 
    packages=find_packages(exclude=['tests*']), 
    license='MIT', 
    description='A journey into the wizarding world', 
    url= 'https://github.com/cfbanks/data-533-lab4',
    author='Connor and Naveen', 
    author_email = 'connorfairbanks@gmail.com' 
)
