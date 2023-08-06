import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='byu-browserstack-helper',
    version='0.3.0',
    author='Mark Roth',
    author_email='mark_roth@byu.edu',
    description='A package for helping with some of the QA teams most used functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/byu-oit/browserstack-helper-library',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License ',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.8',
    install_requires=[
        'boto3 >= 1.16.0, < 1.17.0',
        'Appium-Python-Client >= 1.0.0, < 1.1.0',
        'selenium >= 3.0.0, < 4.0.0'
    ]
)
