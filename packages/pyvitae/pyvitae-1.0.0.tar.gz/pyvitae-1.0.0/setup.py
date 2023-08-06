import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvitae",
    version="1.0.0",
    author="Jin-Hong Du",
    author_email="dujinhong@uchicago.edu",
    description="Model-based Trajectory Inference for Single-Cell RNA Sequencing Using Deep Learning with a Mixture Prior",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaydu1/VITAE",
    packages=setuptools.find_packages(),
    install_requires=[
        "tensorflow >= 2.3.0",
        "tensorflow_probability >= 0.11.0",
        "pandas", 
        "jupyter", 
        "umap-learn", 
        "matplotlib", 
        "numba", 
        "seaborn", 
        "scikit-learn",
        "louvain", 
        "scikit-misc", 
        "networkx" 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)