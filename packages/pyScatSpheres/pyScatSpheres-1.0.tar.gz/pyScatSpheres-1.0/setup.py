import setuptools

#with open("docs/README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="pyScatSpheres",
    version="1.0",
    author="Tarik Ronan Drevon",
    author_email="tarik.drevon@stc.ac.uk",
    description="Scattering of array of spheres, scalar theory",
    long_description='', #long_description,
    long_description_content_type="",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy','scipy','colorama','py3nj','matplotlib'],
)
