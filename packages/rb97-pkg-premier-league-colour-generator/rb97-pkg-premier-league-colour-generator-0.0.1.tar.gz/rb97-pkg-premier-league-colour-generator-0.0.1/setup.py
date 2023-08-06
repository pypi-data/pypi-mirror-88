import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rb97-pkg-premier-league-colour-generator",
    # Replace with your own username above
    version="0.0.1",
    author="Ryan Bannon",
    author_email="ryansbannon@gmail.com",
    description="A small package that retrives the primary colours associated with each of the English Premier League football teams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanbannon/CPP_Project/tree/main/pl_colour_generator",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)