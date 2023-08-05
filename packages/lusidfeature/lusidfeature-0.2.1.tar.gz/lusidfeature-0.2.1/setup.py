from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='lusidfeature',
    version='0.2.1',
    description='This package will allow to run the main file and retrieve a list of decorated feature methods in a cls',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/finbourne/lusid-features-python.git',
    author='FINBOURNE Technology',
    author_email='engineering@finbourne.com',
    license='MIT',
    keywords=["OpenAPI", "FINBOURNE", "LUSID", "LUSID API"],
    packages=['lusidfeature'],
    install_requires=['parameterized>=0.7.4'],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6"
)
