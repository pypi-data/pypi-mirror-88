from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='bbd-table-parser',
    version='0.0.1',
    author='Simon Murphy',
    author_email='murphysimon@outlook.com',
    description='Package to parse inline tables for use with pytest-bdd.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/GreatIrishElk/table_parse',
    packages=find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
    install_requires=[]
)