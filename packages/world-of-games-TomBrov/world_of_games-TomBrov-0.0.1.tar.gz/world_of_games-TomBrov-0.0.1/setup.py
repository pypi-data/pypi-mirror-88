import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="world_of_games-TomBrov", # Replace with your own username
    version="0.0.1",
    author="TomBrov",
    author_email="tbrovy@gmail.com",
    description="Devops course project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TomBrov/WorldOfGames",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
