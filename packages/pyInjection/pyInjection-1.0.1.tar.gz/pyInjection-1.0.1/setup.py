import setuptools #type: ignore

setuptools.setup(
    name="pyInjection",
    version="1.0.1",
    author="Joshua Loader",
    author_email="pyInjection@joshloader.com",
    description="Dependency injection container for Python3",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={
      'pyInjection': ['py.typed'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)