import setuptools
setuptools.setup(
    name="AICloudSDK",
    version="1.0.3",
    author="liyichao",
    author_email="liyichao6852@navinfo.com",
    description="add datatransform folder",
    packages=setuptools.find_packages(),
    package_data={'aicloud': ['datatransform/coco/config.yaml','datatransform/coco/json2coco.py','datatransform/mapillary/config.yaml','datatransform/mapillary/json2mapillary.py','datatransform/voc/*.py','datatransform/voc/config.yaml','datatransform/voc/source/XML_template/voc_template.xml'],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['kafka>=1.3.5', 'redis>=3.5.3'],
    python_requires='>=3')