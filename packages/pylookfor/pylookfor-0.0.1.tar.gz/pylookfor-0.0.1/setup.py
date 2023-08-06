import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylookfor", # Replace with your own username
    version="0.0.1",
    author="yekangq",
    author_email="yekangq@sjtu.edu.cn",
    description="A lightweight module searching methods in the current python environment by keywords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KangqingYe/pylookfor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)