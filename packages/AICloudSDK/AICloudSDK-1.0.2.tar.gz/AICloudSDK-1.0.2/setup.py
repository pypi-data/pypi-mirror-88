import setuptools
setuptools.setup(
    name="AICloudSDK",                                     # 包的分发名称，使用字母、数字、_、-
    version="1.0.2",                                        # 版本号
    author="ai",                                       # 作者名字
    author_email="example@example.com",                      # 作者邮箱
    description="fix bug",                            # 包的简介描述
    packages=setuptools.find_packages(),                    # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，在这种情况下，包列表将是example_pkg
    classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ],
    install_requires=['kafka>=1.3.5', 'redis>=3.5.3'],  # 依赖的包
    python_requires='>=3')