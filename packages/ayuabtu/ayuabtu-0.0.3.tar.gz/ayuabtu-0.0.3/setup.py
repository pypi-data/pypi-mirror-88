import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ayuabtu',
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
    author='Lukas Halbritter',
    author_email='halbi93@gmx.de',
    description='A package for units.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MCHalbi/AllYourUnitAreBelongToUs',
    packages=setuptools.find_packages(),
    classfiers=[
        'Development Status :: 2 - Pre-Alpha'
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
