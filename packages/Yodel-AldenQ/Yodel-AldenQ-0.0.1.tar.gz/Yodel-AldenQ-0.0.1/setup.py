import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Yodel-AldenQ", # Replace with your own username
    version="0.0.1",
    author="Alden Quigley",
    author_email="aldenaquigley@gmail.com",
    description="Yodel is a python library that uses WIFI hardware for remote control purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aldenq/Yodel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.6',
)
