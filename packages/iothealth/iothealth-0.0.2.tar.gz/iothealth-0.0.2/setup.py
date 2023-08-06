"""Setup file for IoT Health."""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="iothealth",
    version="0.0.2",
    description="IoT Health",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/iot-spectator/iot-health",
    author="IoT Spectator",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="IoT",
    packages=setuptools.find_packages(exclude=["examples", "tests"]),
    install_requires=["click", "opencv-python", "psutil"],
    entry_points={"console_scripts": ["iot-health-cli=iothealth.bin.cli:main"]},
    python_requires=">=3.7",
)
