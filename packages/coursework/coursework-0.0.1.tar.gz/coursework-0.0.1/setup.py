from setuptools import setup , find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7'
]

setup(
    name='coursework',
    version='0.0.1',
    description='Model for CRUD operations with PostgreSQL DB',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Andrii Shevliakov',
    author_email='josh@dublocks.org',
    licence='MIT',
    classifiers=classifiers,
    keyword='PostgreSQL',
    packages=find_packages(),
    install_requires=['']
)