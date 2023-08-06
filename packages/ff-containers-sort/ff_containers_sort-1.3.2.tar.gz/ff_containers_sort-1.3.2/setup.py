import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ff_containers_sort", # Replace with your own username
    version="1.3.2",
    author="Naaman Campbell",
    author_email="naaman@clancampbell.id.au",
    description="Sorts and re-numbers Firefox Container config objects in Firefox containers.json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naamancampbell/ff-containers-sort",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS"
    ],
    python_requires='>=3.6',
)