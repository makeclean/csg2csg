import setuptools

long_description = open("README.md").read()

setuptools.setup(
    name="csg2csg",
    version="0.0.27",
    author="andrew davis",
    author_email="andrew.davis@ukaea.uk",
    description="Convert CSG geometry into different formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makeclean/csg2csg",
    packages=setuptools.find_packages(),
    entry_points=dict(console_scripts=["csg2csg=csg2csg.__main__:main"]),
    requires=["numpy"],
    extras_require={
        "dev": ["pytest", "pytest-cov", "ruff"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: License name here",
        "Operating System :: OS Independent",
    ],
)
