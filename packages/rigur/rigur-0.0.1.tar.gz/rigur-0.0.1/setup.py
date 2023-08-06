import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rigur",
    version="0.0.1",
    author="Derek Fujimoto",
    author_email="fujimoto@phas.ubc.ca",
    description="Rip data from images of figures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfujim/rigur",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=['numpy>=1.19','matplotlib>=3.2.2','pandas>=1.0.5'],
    # ~ package_data={'': ['./images']},
    entry_points={'console_scripts':['rigur = rigur:main']},
    # ~ include_package_data=True,
)
