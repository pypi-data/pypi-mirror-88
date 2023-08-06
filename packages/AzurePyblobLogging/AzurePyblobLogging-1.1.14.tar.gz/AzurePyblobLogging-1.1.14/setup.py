import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='AzurePyblobLogging',  
     version='1.1.14',
     author="Jorge Andres Diaz",
     author_email="jorgeandresdn1@gmail.com",
     description="A library to log into blob storage in Azure",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/JorgeDiazz/pyblob_logging",
     py_modules = ['PyblobLogging', 'PyblobLogger', 'BlobDescription'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
