from setuptools import setup, find_packages

with open("curvy/README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="curvy",
        version="0.1.0",
        packages=find_packages(),
        description="Plot model performance",
        url="https://github.com/KimaniKibuthu/curvy",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="br-AI-niac",
        author_email="kimanikibuthu@gmail.com",
        license="MIT",
        zip_safe=False

        )
