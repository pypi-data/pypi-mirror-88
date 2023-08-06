import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zahlabut", # Replace with your own username
    version="0.0.2.17",
    author="Arkady Shtempler",
    author_email="arkadysh@gmail.com",
    description='Extract unique Errors blocks from logs files by given "start time" timestamp',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zahlabut/LogToolPyPi",
    packages=['zahlabut'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='logs, analyze logs, zahlabut, redhat openstack, extract errors from logs',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'GitHub': 'https://github.com/zahlabut/LogTool',
        'Article': 'https://opensource.com/article/20/1/logtool-root-cause-identification',
        'Source': 'https://github.com/zahlabut/LogToolPyPi'}
)



