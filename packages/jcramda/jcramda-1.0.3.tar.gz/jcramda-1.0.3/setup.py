from setuptools import setup, find_packages


# readme = open('Readme.md', 'r').read()


setup(
    name='jcramda',
    version='1.0.3',
    author='Jochen He',
    author_email='thjl@hotmail.com',
    description='functional programming methods',
    long_description='',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'more-itertools',
        'pytz',
        'python-dateutil',
    ],
    python_requires='>=3.6'
)

