from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='autocurve',
    version='0.0.1',
    description='Curve Fitting Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Leonardus Chen',
    author_email='leonardus.chen@gmail.com',
    url='https://github.com/leonarduschen/autocurve',
    license='GPLv3+',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'matplotlib>=3.3.3',
        'numpy==1.19.4',
        'imageio==2.9.0',

    ],
    tests_require=['pytest'],
    packages=find_packages(exclude=('tests', 'docs', 'example')),
)
