import setuptools

long_description = ("PyAutoDiff provides the ability to seamlessly calculate the gradient of a given function within "
                    "your Python code. By using automatic differentiation, this project addresses efficiency and "
                    "precision issues in symbolic and finite differentiation algorithms")

setuptools.setup(
    name="4dpyautodiff",
    version="1.0.0",
    author="cs107-JTGC",
    author_email="chenfanzhuang@g.harvard.edu",
    description="A simple library for auto differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cs107-JTGC/cs107-FinalProject",
    packages=setuptools.find_packages(exclude=['docs', 'tests*', 'scripts']),
    install_requires=[
        "numpy",
        "graphviz"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
