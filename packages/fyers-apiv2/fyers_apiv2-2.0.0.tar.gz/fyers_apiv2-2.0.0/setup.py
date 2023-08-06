import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='fyers_apiv2',  
     version='2.0.0',
     author="Fyers-Tech",
     author_email="support@fyers.in",
     description="Fyers trading APIs.",
     long_description="",
     long_description_content_type="text/markdown",
     url="https://github.com/FyersDev/fyers-api-py",
     packages=setuptools.find_packages(),
     install_requires=[
              'requests',
              'tornado'
          ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
