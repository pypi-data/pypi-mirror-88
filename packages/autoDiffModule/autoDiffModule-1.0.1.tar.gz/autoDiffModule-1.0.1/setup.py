import setuptools
  
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoDiffModule",
    version="1.0.1",
    author="Christopher Chen, Avriel Epps-Darling, Pawel Nawrocki, Matthew Quesada",
    author_email="christopher_chen@college.harvard.edu",
    description="An automatic differentiation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PST-philz-sushi-tacos/cs107-FinalProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

