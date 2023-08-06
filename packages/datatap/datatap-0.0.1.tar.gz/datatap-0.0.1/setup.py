import setuptools

long_description = """
# Datatap

Visit [datatap.dev](http://datatap.dev) for more details
"""

setuptools.setup(
    name = "datatap",
    version = "0.0.1",
    author = "Zensors' Dev Team",
    author_email = "datatap@zensors.com",
    description = "Client library for dataTap",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://zensors.com",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.7",
)