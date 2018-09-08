import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='agree',
    version='0.0.1',
    description='Visual and statistical assessment of annotator agreements',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Oliver Price',
    author_email='op.oliverprice@gmail.com',
    url='https://github.com/o-P-o/agree',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=['agree']
)
