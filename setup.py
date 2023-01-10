from setuptools import setup, find_packages


setup(
    name="seferelation",
    version="0.0.1",
    packages=find_packages(),
    url="https://github.com/ykaner/relation-project",
    license="",
    author="ykaner",
    author_email="ykaner12@gmail.com",
    description="Find relations in the jewish library",
    install_requires=[
        "tqdm",
    ],
    entrypoint={
        'console_scripts': ['seferelation = seferelation.main:main']
    },
)
