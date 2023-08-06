import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concentrator-calculator",
    version="1.0.1",
    author="Dominik Buchner",
    author_email="dominik.buchner524@googlemail.com",
    description="Tool to calculate vacuum centrifuge times",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DominikBuchner/concentrator_calculator",
    packages=setuptools.find_packages(),
    license = 'MIT',
    install_requires = ['PySimpleGUI >= 4.19.0',
                        'numpy >= 1.18.4',
                        'pandas >= 1.0.4',
                        'scipy >= 1.4.1'],
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        "console_scripts" : [
            "concentrator_calculator = concentrator_calculator.__main__:main",
        ]
    },
)
