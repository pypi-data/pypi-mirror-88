import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nbmc",
    version="0.0.2",
    description="Executes Yosys BMC and renders counterexample as SVG",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nturley/nmbc",
    author="Neil Turley",
    author_email="neilpturley@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=['nbmc'],
    include_package_data=True,
    install_requires=[
        "yowasp-yosys",
        "wavedrom",
        "z3-solver",
        "pyDigitalWaveTools",
        "parse"
    ]
)