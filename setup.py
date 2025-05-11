from setuptools import setup, find_packages

setup(
    name="ocelytics",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scipy"
    ],
    author="Sabrine",
    description="Object-centric event log feature extractor",
)
