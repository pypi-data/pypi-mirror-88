from setuptools import setup, find_packages


with open("README.md", "rb") as f:
    long_description = f.read().decode("utf8")


setup(
    name="GA-Common",
    version="0.1",
    author="lipo",
    author_email="lipo8081@gmail.com",
    description="Easy Use GA",
    url="https://github.com/lipopo/ga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>3.0'
)
