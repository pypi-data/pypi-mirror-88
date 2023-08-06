import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CityAD", 
    version="0.1.2",
    author="Group CityScape",
    author_email="cityad.helpline@gmail.com",
    description="CityAD, an Automatic Differentiation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cityscape-107/cs107-FinalProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy==1.18.0']
)