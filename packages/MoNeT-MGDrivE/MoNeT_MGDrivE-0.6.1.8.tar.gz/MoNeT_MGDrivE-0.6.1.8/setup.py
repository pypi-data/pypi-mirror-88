import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='MoNeT_MGDrivE',
    version='0.6.1.8',
    url='https://github.com/Chipdelmal/MoNeT_MGDrivE',
    author='Hector M. Sanchez C.',
    author_email='sanchez.hmsc@berkeley.edu',
    description="MoNeT python package for MGDrivE data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy', 'scipy', 'matplotlib', 'ipython',
        'jupyter', 'pandas', 'sympy', 'compress-pickle'
    ],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
 )