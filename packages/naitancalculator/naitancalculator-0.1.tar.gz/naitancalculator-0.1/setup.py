from setuptools import setup, find_packages
 
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

setup(
    name='naitancalculator',
    version='0.1',
    description='A very basic calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='Aditya Naitan',
    author_email='adityanaitan@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['calculator', 'naitancalculator', 'add', 'substract', 'multiply', 'divide'], 
    packages=find_packages(),
    install_requires=[''],
)