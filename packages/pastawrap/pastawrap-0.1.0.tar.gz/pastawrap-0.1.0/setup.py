import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pastawrap",
    version="0.1.0",
    author="Davor Virag, Ivan Kodvanj, Jan Homolak",
    author_email="davor.virag@gmail.com",
    maintainer="Davor Virag",
    maintainer_email="davor.virag@gmail.com",
    description="The Python wrapper for ratPASTA - R-based Awesome Toolkit for PASTA.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davorvr/pastawrap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: R",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering"
    ],
    python_requires=">=3.8",
    install_requires=["rpy2>=3.3.0",
                      "pandas>=1.0.0"]
)