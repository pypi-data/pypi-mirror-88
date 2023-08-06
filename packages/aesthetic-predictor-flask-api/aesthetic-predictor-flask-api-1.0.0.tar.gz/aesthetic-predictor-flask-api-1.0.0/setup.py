import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()


setuptools.setup(
    name="aesthetic-predictor-flask-api",  # Replace with your own username
    version="1.0.0",
    author="Ribin Chalumattu",
    description="Package for sharing flask api for aesthetic predictors.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7'
)
