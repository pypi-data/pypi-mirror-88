import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adk",
    version="0.0.3",
    author="Attoy",
    author_email="attoy@hotmail.com",
    description="A ADK-dev Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qsrc/ADK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": ["adk = adk.rpc.rpc_service:main"],
        "gui_scripts": ["adk.d = adk.rpc.rpc_service:main"],
    },
)
