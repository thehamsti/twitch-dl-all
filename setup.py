from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="twitch-dl-all",
    version="0.1.0",
    author="hamsti",
    description="A tool to download all highlights and uploads from a Twitch channel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hamsti/twitch-dl-all",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "twitch-dl>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "twitch-dl-all=twitch_dl_all.cli:main",
        ],
    },
) 