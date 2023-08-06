import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exception_convenience",
    version="0.1.0",
    author="Adrian Thoenig",
    description="Convenience collection of exceptions which often go together. Avoiding to broad exception clauses but still catching everything",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThoenigAdrian/exception_convenience",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.5',
    setup_requires=['wheel'],
)
