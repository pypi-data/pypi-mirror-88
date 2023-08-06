import setuptools

setuptools.setup(
    name="SeeSun",
    version="0.0.1",
    license='MIT',
    author="A-eye",
    author_email="leey93ssu@gmail.com",
    description="Package for building service based on speech recognition/synthesis , Object detection , OCR",
    long_description_content_type='text/markdown',
    long_description=open('README.md',encoding='utf-8').read(),
    url="https://github.com/ineed-coffee?tab=repositories",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
