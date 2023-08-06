import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="somappy",
    version="0.1.0",
    entry_points = {
        'console_scripts': ['somappy=somappy.som_selector_gui:main']},
    author="Doug Denu",
    author_email="dcdenu4@gmail.com",
    description="A Self Organizing Map library based on R-Kohonen.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcdenu4/somappy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
