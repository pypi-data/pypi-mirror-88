##########################
# Imports
##########################


# Global
import setuptools

# Local
import few_shots_clf


##########################
# Setup
##########################


# Install requirements
with open("./requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().split("\n")[:-1]


# Long description
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


# Download url
GITHUB_URL = "https://github.com/delmalih/few-shots-classification"
DOWNLOAD_VERSION = few_shots_clf.__version__.replace(".", "")
DOWNLOAD_URL = f"{GITHUB_URL}/archive/v_{DOWNLOAD_VERSION}.tar.gz"


setuptools.setup(
    name="few_shots_clf",
    version=few_shots_clf.__version__,
    author=few_shots_clf.__author__,
    author_email=few_shots_clf.__author_email__,
    description=few_shots_clf.__description__,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    download_url=DOWNLOAD_URL,
    packages=setuptools.find_packages(),
    license="LICENSE.txt",
    install_requires=requirements,
    python_requires=">=3.6, <3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.6",
    ],
    keywords=[
        "FEW-SHOTS",
        "CLASSIFICATION",
        "IMAGE",
        "COMPUTER VISION"
    ],
)
