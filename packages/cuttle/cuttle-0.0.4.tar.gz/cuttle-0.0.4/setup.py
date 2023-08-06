from setuptools import setup, find_packages

setup(
    name='cuttle',
    version='0.0.4',
    author="Karishnu Poddar",
    author_email="karishnu@gmail.com",
    py_modules=['script'],
    package_dir={'': 'src'},
    packages=[''],
    install_requires=[
        'Click',
        'paramiko',
        'scp',
        'nbformat',
        'nbconvert',
        'ipython'
    ],
    entry_points='''
        [console_scripts]
        cuttle=script:cli
    ''',
)