from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ALMA-app",
    version="0.1.0",
    author="Francisco Marchi",
    description="A package for generating ALMA plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/f-marchi/ALMA-app",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "pandas",
        "bokeh",
    ],
)