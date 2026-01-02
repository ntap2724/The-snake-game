from setuptools import setup, find_packages

setup(
    name="thesnakegame",
    version="1.0.0",
    description="A classic Snake game implementation in Python",
    author="Developer",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pygame>=2.5.3",
        "setuptools",
        "wheel",
    ],
    entry_points={
        "console_scripts": [
            "snakegame=src.main:run",
        ],
    },
)
