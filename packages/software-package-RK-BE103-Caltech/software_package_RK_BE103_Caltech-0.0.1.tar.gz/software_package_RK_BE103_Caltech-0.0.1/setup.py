import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='software_package_RK_BE103_Caltech',
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