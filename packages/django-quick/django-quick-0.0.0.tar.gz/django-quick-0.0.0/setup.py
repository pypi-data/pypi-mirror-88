import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-quick",
    version="0.0.0",
    author="Feiox",
    author_email="fei2037@gmail.com",
    description="Simplify django development experience",
    keywords="django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feiox/django_quick",
    packages=setuptools.find_packages(),
    install_requires=[
        'django>=3.1.0',
    ],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ),
)
