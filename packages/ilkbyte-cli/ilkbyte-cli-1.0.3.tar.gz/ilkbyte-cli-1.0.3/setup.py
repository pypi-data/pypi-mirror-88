import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="ilkbyte-cli",
    version="1.0.3",
    author="Türkalp Burak Kayrancıoğlu",
    author_email="bkayranci@gmail.com",
    description="Ilkbyte python CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkayranci/ilkbyte-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
              'console_scripts': [
                  'ilkbyte = ilkbyte_cli.main:main',
              ],
          },
)
