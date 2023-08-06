from setuptools import setup
from mineflex import __version__

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()


readme = ""
with open("README.md") as f:
    readme = f.read()


setup(
    name="mineflex-py",
    author="Pnlmon",
    url="https://github.com/Pnlmon/mineflex-py",
    version=__version__,
    packages=["mineflex"],
    license="MIT",
    description="Mineflex API Wrapper written in python",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires=">=3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
