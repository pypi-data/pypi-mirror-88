import setuptools
 
setuptools.setup(
    name="NCMB",
    version="1.2.0",
    author="goofmint",
    author_email="atsushi@moongift.jp",
    description="NCMB is client SDK for Nifcloud mobile backend",
    long_description="NCMB is client SDK for Nifcloud mobile backend. It supports Data store, File store, Authentication, Script and etc.",
    long_description_content_type="text/markdown",
    url="https://mbaas.nifcloud.com/",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)