from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "telegram-coffee-break",
    version = "0.2.1",
    author = "Romain Gratier",
    author_email = "romain.gratier@gmail.com",
    url = "https://github.com/RomainGratier/telegram-coffee-break",
    description = ("send telegram notification using a bot"),
    license = "MIT",
    keywords = "python telegram",
    py_modules=["telegrambotalarm", "message"],
    package_dir={"": "telegrambotalarm"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires = [
        "requests>=2.25.0",
    ],
)

