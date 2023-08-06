import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_shotgun", # Replace with your own username
    version="0.0.1",
    author="Noflame Lin",
    author_email="linjuang@gmail.com",
    description="simple shotgun api wrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/MoonShineVFX/py_shotgun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
