from setuptools import setup

setup(name='sopic',
    version='0.0.2',
    description='Helper for manufacturing station',
    install_requires=[
        'PyQt5==5.13.1',
        'colorlog==4.1.0',
    ],
    packages=['sopic'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
