import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezhook", 
    version="0.0.2",
    author="RJSON LABS",
    description="Send discord webhooks in python with 2 lines of code!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rjson.dev/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp','discord.py'],
    python_requires='>=3.6',
)
