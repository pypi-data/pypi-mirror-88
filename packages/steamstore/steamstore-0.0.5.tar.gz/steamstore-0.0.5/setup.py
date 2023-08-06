from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name="steamstore",
    version="0.0.5",
    author="Sauce",
    author_email="saucesteals@gmail.com",
    description="A Python wrapper for the Public Steam StoreFront API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/saucesteals/steamstore",
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
)