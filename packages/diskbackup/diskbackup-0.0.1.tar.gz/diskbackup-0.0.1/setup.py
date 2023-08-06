from setuptools import setup

setup(
    name='diskbackup',
    version='0.0.1',
    author="Joseph Ernest",
    author_email="nouvellecollection@gmail.com",
    description="Simple backup tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/josephernest/diskbackup",
    platforms='any',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    py_modules=['diskbackup'],
    install_requires=[],
    python_requires='>=3.6'
)