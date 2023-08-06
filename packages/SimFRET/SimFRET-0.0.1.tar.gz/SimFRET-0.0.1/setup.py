import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimFRET",
    version="0.0.1",
    author="Diego Kleiman",
    author_email="diegokleiman@hotmail.com",
    description="A Python package to simulate FRET experiments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegoeduardok/SimFRET",
    packages=setuptools.find_packages(),
    # package_dir={
    #     'simfret': 'src',
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.6',
)
