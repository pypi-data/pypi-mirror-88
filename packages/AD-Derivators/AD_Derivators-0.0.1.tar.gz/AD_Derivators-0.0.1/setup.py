import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AD_Derivators",
    version="0.0.1",
    author="Alice Li, Ethan Schumann, Ruizhe Kang, Vikram Shastry",
    author_email="anqili@g.harvard.edu",
    description="Auto-Differentiation Package based on Forward Mode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DERIVATORS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)