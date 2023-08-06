import setuptools
from setuptools import setup, Extension

with open("README.md", "r", encoding="UTF-8") as file:
    longDescription = file.read()

def generateModule():
    setup(
          name="fputs",
          version="1.0.0",
          description="Python interface for the fputs C library function",
          long_description=longDescription,
          long_description_content_type="text/markdown",
          url="https://github.com/MahanthMohan/fputsModule",
          classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3",
            "Programming Language :: C",
          ],
          python_requires='>=3.6',
          author="Mahanth Mohan",
          author_email="mohan.mahanth@gmail.com",
          ext_modules=[Extension("fputs", ["fputsModule.c"])]
        )

if __name__ == "__main__":
    generateModule()
