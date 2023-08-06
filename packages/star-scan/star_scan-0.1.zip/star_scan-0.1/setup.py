from distutils.core import setup

setup(
    name='star_scan',
    version='0.1',
    license='MIT',
    description='Simple port scanning module',
    author='Wesley Reid',
    author_email='wesleyreid0@gmail.com',
    url='https://github.com/starhound/star_scan',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['NETWORK', 'UTILITY', 'PORT SCANNER'],
    install_requires=[
        'socket',
        'sys',
        'ipaddress',
        'logging',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
