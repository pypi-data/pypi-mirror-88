import setuptools
from shooki.version import version

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="shooki",
    version=version,
    author="Gilad Kutiel",
    author_email="gilad.kutiel@gmail.com",
    description="html in python",
    long_description=long_description,
    long_description_content_type='text/markdown',    
    url="https://github.com/shooki/shooki",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[]
)
