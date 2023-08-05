import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="falib", # Replace with your own username
    version="0.0.2",
    author="zuel_quant_lab",
    author_email="505871220@qq.com",
    description="calculate quant factor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/jiangwenhao123/falib.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)