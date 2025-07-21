from setuptools import setup, find_packages

setup(
    name="os-flip",
    version="1.0.3",
    description="Cross-platform boot OS selector for Linux, Windows, and macOS",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AK",
    author_email="herogupta626@email.com",
    url="https://github.com/AKris15/OS-Flip",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "os-flip=os_flip.__main__:main"
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
)
