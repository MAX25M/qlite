from setuptools import setup, find_packages

setup(
    name="qlite",
    version="1.0.0",
    author="Mark Joseph N. Octavo",
    description="A modular, mobile-friendly Quantum Compiler and Simulator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MAX25M/qlite",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "ply>=3.11",
    ],
    entry_points={
        "console_scripts": [
            "qlite=cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.8',
)
