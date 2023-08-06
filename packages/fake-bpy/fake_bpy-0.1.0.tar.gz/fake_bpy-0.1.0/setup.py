import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fake_bpy",
    version="0.1.0",
    author="Arjun Sahlot",
    author_email="iarjun.sahlot@gmail.com",
    description="Module with various useful utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArjunSahlot/",
    py_modules=["fake_bpy"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)
