import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hxtz", 
    version="1.0.3",
    author="hxtz",
    author_email="1375151810@qq.com",
    description="me",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cn.bing.com/",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests","pandas" # 封装的包所依赖的基础三方库
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
      
