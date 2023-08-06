import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='sprkBE103cit',
    version='0.0.1',
    author='Rohit Kantipudi',
    author_email='rohitk@caltech.edu',
    description='Package created for extra-credit assignment be103a team 18 to analyze microtubule catastrophe.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=["numpy","pandas", "bokeh>=1.4.0"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)