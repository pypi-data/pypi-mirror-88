import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rocketchat_bot_simple_app_bot",
    version="0.1.0",
    author="Pavel Khorikov",
    author_email="lev@ph3.ru",
    description="Bot client for rocketchat BotBridgeApp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JargeZ/RocketChat-Simple-AppBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'Webhook-Listener',
          'loguru',
      ],
    python_requires='>=3.8',
)