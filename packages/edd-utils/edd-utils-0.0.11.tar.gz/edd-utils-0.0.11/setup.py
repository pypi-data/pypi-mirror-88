import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edd-utils",
    version="0.0.11",
    author="Zak Costello, William Morrell, Mark Forrer, Tijana Radivojevic, Reinhard Gentz",
    author_email="tradivojevic@lbl.gov",
    description="Download Studies from an Experiment Data Depot Instance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBEI/edd-utils",
    packages=setuptools.find_packages(),
    python_requires=">=3.6.5",
    install_requires=["tqdm>=4.25.0","pandas","requests"],
    entry_points = {
        "console_scripts": ["export_edd_study=edd_utils:commandline_export"],
    },
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
    ],
)