import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='settings-jc',
    version="0.0.2",
    author="Jim Carter",
    author_email="jcarter62@gmail.com",
    description="Application Settings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jcarter62/settings_jc.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['cryptography', 'getmac','arrow']
)
