import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beltosbml",
    version="0.0.6",
    author="Bradley Wililam English",
    author_email="brad.w.english@gmail.com",
    description="Package to extend a SBML model with BEL queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VitaminBrad/BELtoSBML",
    packages=['beltosbml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
