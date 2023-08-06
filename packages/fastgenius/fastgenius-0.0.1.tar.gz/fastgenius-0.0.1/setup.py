from setuptools import find_packages, setup
from fastgenius import __version__, __url__, __author__, __description__, __license__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


extras_require = {"docs": ["sphinx~=3.2", "sphinx-rtd-theme",]}
extras_require["dev"] = extras_require["docs"]


setup(
    name="fastgenius",
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=__license__,
    author=__author__,
    author_email="contacttheomartin+fastgenius@gmail.com",
    url=__url__,
    keywords="genius api genius-api music lyrics artists songs fast async python wrapper",
    packages=find_packages(exclude=["tests"]),
    install_requires=["beautifulsoup4>=4.6.0", "requests>=2.20.0"],
    extras_require=extras_require,
    classifiers=[
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
