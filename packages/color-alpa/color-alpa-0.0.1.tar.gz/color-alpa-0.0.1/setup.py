import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="color-alpa", # Replace with your own username
    version="0.0.1",
    author="Albert Pang",
    author_email="alpaaccount@mac.com",
    description="ANSI Color hightlight",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alpaalpa/color",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
