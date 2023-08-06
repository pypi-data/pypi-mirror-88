from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='reason',
    version='0.0.1',
    description='Machine Learning Toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alisoltanirad/Reason',
    author='Ali Soltani Rad',
    author_email='soltaniradali@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy'
    ]
)
