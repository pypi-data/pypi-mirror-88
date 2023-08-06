import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylcanim", 
    version="0.0.4",
    author="lioncat2002",
    author_email="gamedevcorp2002@gmail.com",
    description="A simple library for loading animations made with SpriteFactory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lioncat2002/pylcanim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
