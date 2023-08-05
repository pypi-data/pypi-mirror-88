import os
import sys
import setuptools

with open(os.path.join(sys.path[0], "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="file-wizard",
    version="1.0.1",
    author="S Krishna Bhat, Pankaj Kumar G",
    author_email="ccrc@fisat.ac.in",
    description="A basic file handler for python tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/file-wizard/file-wizard",
    install_requires=[
          'shutils',
      ],
    packages=setuptools.find_packages(),
    # entry_points={
    #     'console_scripts': ['pdfcc = pdfcc.pdfcc:main']
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
