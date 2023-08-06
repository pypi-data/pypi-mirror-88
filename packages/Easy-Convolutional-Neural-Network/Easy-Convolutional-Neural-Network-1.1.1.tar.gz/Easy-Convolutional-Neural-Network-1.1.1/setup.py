from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="Easy-Convolutional-Neural-Network",
    version="1.1.1",
    description="Simplify the creation of convolutional neural network",
    py_modules=["ECNN"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "numpy ~= 1.19",
    ],
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    url="https://github.com/alix59/ECNN",
    author="Hamidou Alix",
    author_email="alix.hamidou@gmail.com",
)