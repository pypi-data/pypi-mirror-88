import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyscraper",
    version="0.0.1",
    author="yishai rasowsky",
    author_email="yishairasowsky@gmail.com",
    description="scrape images relevant to your text passage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yishairasowsky/easyscraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
