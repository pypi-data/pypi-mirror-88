import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UnpackIPs",
    version="2.0.2",
    author="cober2019",
    author_email="cober91130@gmail.com",
    description="Allow a user to unpack IP ranges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cober2019/UnpackIPs",
    packages=setuptools.find_packages(),
    install_requires=['ipaddress'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)