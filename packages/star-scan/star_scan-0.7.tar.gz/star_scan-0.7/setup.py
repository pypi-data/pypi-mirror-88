import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='star_scan',
    version='0.7',
    license='MIT',
    description='Simple port scanning module',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Wesley Reid',
    packages=["star_scan"],
    author_email='wesleyreid0@gmail.com',
    url='https://github.com/starhound/star_scan',
    download_url='https://github.com/starhound/star_scan/archive/main.zip',
    keywords=['NETWORK', 'UTILITY', 'PORT SCANNER'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
