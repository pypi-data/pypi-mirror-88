import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ttdet', 
    version='1.0.9',
    author="Trung M. Bui",
    author_email="bmtrungvp@gmail.com",
    description="A vision utilities for computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtbui2010",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT', 
    keywords = ['AI','DETECTION', 'UTILITY'],
    install_requires=[            
          'numpy',
        'opencv-python',
         'scipy',
         'matplotlib'
     ],
)	
