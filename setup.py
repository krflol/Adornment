from setuptools import setup, find_packages

setup(
    name="adornment",
    version="0.1",
    packages=find_packages(),
    author="Keenan Finkelstein",
    author_email="keenanfinkelstein@gmail.com",
    description="A collection of llm decorators.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="http://github.com/yourusername/my_package",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)