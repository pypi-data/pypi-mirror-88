import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taskframe",
    version="0.1.12",
    author="Denis Vilar",
    description="Taskframe Python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Taskframe/taskframe-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests>=2.4.2", "ipython>=5.5.0"],
    python_requires=">=3.6",
)
