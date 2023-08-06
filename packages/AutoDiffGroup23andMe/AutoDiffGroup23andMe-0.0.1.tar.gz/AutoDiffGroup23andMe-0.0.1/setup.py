import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="AutoDiffGroup23andMe",
    version="0.0.1",
    author="Omead Eftekhari, Drew Pendergrass, Saul Soto, Ryan Liu",
    author_email="",
    description="An optimization tool-kit package utilizing automatic differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Group23andMe/cs107-FinalProject",
    packages=['AutoDiffGroup23andMe'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)