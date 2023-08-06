import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dccl",
    version="0.0.2",
    author="Niklas Salmoukas",
    author_email="niklas@salmoukas.com",
    description="Connect to any DCC tool from anywhere.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coreprocess/dccl/dccl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    license="LGPLv3",
    python_requires='>=3.6',
)