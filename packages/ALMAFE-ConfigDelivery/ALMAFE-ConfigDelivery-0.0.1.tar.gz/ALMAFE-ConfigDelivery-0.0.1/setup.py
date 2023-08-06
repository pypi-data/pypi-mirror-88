import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ALMAFE-ConfigDelivery",
    version="0.0.1",
    author="Morgan McLeod",
    author_email="mmcleod@nrao.edu",
    description="Classes for retrieval and transformation of ALMA Front End subassembly configuration data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/morganmcleod",
    packages=setuptools.find_packages(),
    install_requires=[
        'ALMAFE-Lib>=0.0.2',
        'plotly>=4.9.0',
        'pandas>=1.1.3',
        'psutil>=5.7.2'
    ],
    package_data={'ConfigDelivery' : ['CCA6/ConfigFiles/*']},
    data_files=[('.',['ConfigDelivery_template.ini'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)