import setuptools

with open("../docs/documentation.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodiff-djw", # Replace with your own username
    version="0.1.3",
    author="David Chataway, Javiera Astudillo, Wenhan Zhang",
    author_email="jastudillo@g.harvard.edu",
    description="Automatic differentiation package AC207",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DJ-WJ/cs107-FinalProject",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
          'scipy'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)