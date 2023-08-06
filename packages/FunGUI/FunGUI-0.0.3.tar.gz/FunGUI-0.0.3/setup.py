import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FunGUI", # Replace with your own username
    version="0.0.3",
    author="shawn yan wang",
    author_email="shawnyanwang@gmail.com",
    description="It is a tool to easily generate GUI from a function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/shawnyanwang/fun_-gui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'matplotlib>=3.1.0',
    ],
    python_requires='>=3.6',
)
