import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-circuit-sim",
    version="0.0.0",
    author="KrazyKirby99999",
    description="An open-source project to simulate logic gates and other circuits in Python3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KrazyKirby99999/py-circuit-sim/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose2.collector.collector',
)