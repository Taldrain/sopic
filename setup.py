from setuptools import setup

setup(
    name='sopic',
    version='0.1.0',
    description='Helper for manufacturing station',
    install_requires=[
        'PyQt5==5.*',
        'colorlog==4.1.0',
        'pygraphviz==1.6',
    ],
    packages=['sopic', 'sopic.gui', 'sopic.utils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
