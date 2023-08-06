import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dictionaryio",
    version="0.0.1",
    author="Lucky Adogun",
    author_email="meetluckyadogun@gmail.com",
    description="An English dictionary wrapper with voice-pronunciation enabled",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luckyadogun/dictionaryIO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)