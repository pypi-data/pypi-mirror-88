import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="nocloud",
    version="0.0.1",
    author="jonathan lung",
    author_email="lungj@heresjono.com",
    description="Tools for creating a NoCloud image.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lungj/nocloud",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        "pycdlib",
        "pyvhd",
    ]
)