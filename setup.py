from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Medical-Diagnosis",
    version="0.1.1",
    author="Akash",
    packages=find_packages(),
    install_requires = requirements,
)