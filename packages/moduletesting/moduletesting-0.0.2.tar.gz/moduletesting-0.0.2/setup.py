from setuptools import setup,find_packages

classifiers =[
    'Development Status :: 5 - Production/testing',
    'Intended Audience :: Education',
    'Operating System :: MacOS :: MacOS Big Sur :: 11.0 Beta (20A5374i)',
    'License :: OSI Approved :: MIT License',
    ' Programingb Language :: Python :: 3'
]

setup(
    name='moduletesting',
    version='0.0.2',
    description='A simple calculator to test the creation of a python module',
    long_description= open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ulysses-Pacome Koudou',
    author_email='up.koudou@gmail.com',
    license='MIT',
    classifier=classifiers,
    Keywords='',
    packages=find_packages(),
    install_requires=['']
)