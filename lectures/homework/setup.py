from setuptools import setup

setup(
    name='tagcounter',
    version='1.0',
    author='Elena_Shmidt',
    packages=['tagcounter'],
    description='Description',
    package_data={'': ['*.txt']},
    # install_requires=['requests', 'tkinter', 'bs4', 'sqlite3', 'pickle'],
    entry_points={'console_scripts':
                      ['tagcounter = tagcounter.tagcounter:main',
                       'manage_synonyms = tagcounter.tagcounter:manage_alias']},
)
