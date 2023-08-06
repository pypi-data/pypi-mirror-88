import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc_aircraft_campaign",
    version="0.2",
    author="xuetianyin",
    author_email="zuiwo9@outlook.com",
    description="aircraft_campaign",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pgzero>=1.2'],
    entry_points={
        'console_scripts': [
            'mc_aircraft_campaign=mc_aircraft_campaign:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)