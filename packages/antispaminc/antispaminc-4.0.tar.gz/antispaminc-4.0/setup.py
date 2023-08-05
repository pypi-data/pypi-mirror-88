import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="antispaminc",
    version="4.0",
    author="Leo",
    url="http://antispaminc.tk",
    license='License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    author_email="dev@antispaminc.tk",
    description="A Python Wrapper For Antispam Inc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["requests >= 2.22.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)