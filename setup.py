from setuptools import setup

setup(
    name="TIFFany",
    version="0.1",
    description="Media Library powered by the Raspberry Pi.",
    author="Dan Stoakes",
    author_email="dan.stoakes8@gmail.com",
    license="MIT",
    packages=find_packages(include=["Sigourney"]),
    install_requires=[
        "flask",
        "dotenv",
        "functools"
    ],
    zip_safe=False
)