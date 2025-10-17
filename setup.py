from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="makeimpact",
    version="1.2.0",
    author="1ClickImpact",
    author_email="contact@1clickimpact.com",
    description="Python SDK for 1ClickImpact API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1ClickImpact/makeimpact-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.0.0",
    ],
)
