import setuptools

setuptools.setup(
    name="moonshine-node",
    version="0.0.5",
    author="eli Hung",
    author_email="mrhchief@gmail.com",
    description="toolkit for moonshine node-server",
    long_description="toolkit for moonshine node-server",
    long_description_content_type="text/plain",
    url="https://github.com/MoonShineVFX/node-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Flask',
        'requests',
        'pymongo'
    ]
)