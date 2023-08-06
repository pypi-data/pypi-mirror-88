import setuptools
import uuid
import time


def versionme():
    curr_time = time.gmtime()
    nowy = int(curr_time.tm_year)
    nowm = int(curr_time.tm_mon)
    nowd = int(curr_time.tm_mday)
    nowhour = int(curr_time.tm_hour)
    nowmin = int(curr_time.tm_min)
    nowsec = int(curr_time.tm_sec)

    vy = (nowy - 2020)
    vm = (nowm - 12)
    vd = (nowd - 16)
    vp = '{}{}{}'.format(nowhour, nowmin, nowsec)
    vp = int(vp)
    return '{}.{}.{}.{}'.format(vy, vm, vd, vp)

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nnbnonaybay',
    version=versionme(),
    author='nonaybay',
    author_email='rafaelvenancio@protonmail.com',
    description='Basicão',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[
        'pick',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
)
