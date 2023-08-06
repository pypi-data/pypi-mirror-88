import setuptools

setuptools.setup(
    name="wwc129",
    version="0.0.3",
    author='wwc129',
    author_email='wwc129@gmail.com',
    description='test',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'wwc129=main:main'
        ]
    }
)
