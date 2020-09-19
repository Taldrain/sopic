from setuptools import setup

setup(
    name='sopic',
    version='0.0.8',
    description='Helper for manufacturing station',
    install_requires=[
        'PyQt5==5.*',
        'colorlog==4.1.0',
    ],
    packages=['sopic', 'sopic.gui', 'sopic.utils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
