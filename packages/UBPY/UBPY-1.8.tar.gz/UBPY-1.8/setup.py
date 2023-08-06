import setuptools

setuptools.setup(
    name="UBPY",
    version="1.8",
    license='MIT',
    author="Gawi_pr",
    author_email="popop098@naver.com",
    description="UniqueBot python SDK",
    long_description=open('README.md', 'rt', encoding='UTF8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/popop098/UBPY",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp',
    ],
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
