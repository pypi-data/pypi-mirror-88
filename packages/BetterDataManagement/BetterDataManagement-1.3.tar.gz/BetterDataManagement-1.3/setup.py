import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BetterDataManagement", # Replace with the pkg name
    version="1.3",
    author="Alexandre Silva // MrKelpy",
    author_email="alexandresilva.coding@gmail.com",
    description="A Package designed for a better data management when it comes to both files and directories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrKelpy/betterdatamanagement",
    packages=setuptools.find_packages(),
    install_requires=["binaryornot"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)