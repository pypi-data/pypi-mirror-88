import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="futeamigos",
    version="0.0.1",
    author="patrickctrf",
    author_email="patrickctrf@gmail.com",
    description="Package for Reinforcement Learning in MO436-UNICAMP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/patrickctrf/mo436-project-01",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
