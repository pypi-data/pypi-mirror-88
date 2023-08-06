from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name="imgflip",
    version="0.0.1",
    author="axju",
    author_email="moin@axju.de",
    description="api to imgflip",
    long_description=readme(),
    long_description_content_type='text/x-rst',
    url="https://github.com/axju/imgflip",
    packages=['imgflip'],
    install_requires=[
        'requires'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
