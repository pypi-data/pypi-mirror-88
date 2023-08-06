from setuptools import setup, find_packages

setup(
    name='less.cli',
    url='https://github.com/pashabitz/less.cli',
    author='less',
    author_email='pavelbitz@gmail.com',
    py_modules=['less'],
    packages=find_packages(),
    install_requires=['requests', 'Click', ],
    entry_points={
        'console_scripts': [ 
            'less = less.cli.cli:main' 
        ] 
    },
    version='0.1.3',
    license='GPL3',
    description='Command line interface for less',
)