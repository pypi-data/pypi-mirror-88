import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fake_therm_w1_slave_tvanroon",
    version="0.2",
    author="Ted van Roon",
    author_email="tvanroon@gmail.com",
    description="fake_therm_w1_slave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/djtt/fake_therm_w1_slave/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)