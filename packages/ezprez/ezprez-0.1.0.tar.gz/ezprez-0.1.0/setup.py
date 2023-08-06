"""Contains all the configuration for the package on pip"""
import setuptools

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string

    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "ezprez", 
    version = "0.1.0", 
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "An object based api for generating web presentations/slideshows",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    project_urls = {
        "User Docs" :      "https://ezprez.readthedocs.io",
        "API Docs"  :      "https://kieranwood.ca/ezprez",
        "Source" :         "https://github.com/Descent098/ezprez",
        "Bug Report":      "https://github.com/Descent098/ezprez/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D",
        "Feature Request": "https://github.com/Descent098/ezprez/issues/new?labels=enhancement&template=feature_request.md&title=%5BFeature%5D",
        "Roadmap":         "https://github.com/Descent098/ezprez/projects"
    },
    include_package_data = True,
    packages = setuptools.find_packages(),
    install_requires = [
    "pystall", # Used to install webslides
    "elevate", # Used to elevate permissions for protected folder access
    "tqdm"     # Used for progress bars
        ],
    extras_require = {
        "dev" : ["pytest", # Used to run the test code in the tests directory
                "mkdocs"], # Used to create HTML versions of the markdown docs in the docs directory
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
)