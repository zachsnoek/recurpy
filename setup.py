from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="recurpy",
    version="0.0.1",
    description="Easily add events with recurring times to your Google Calendar.",
    url="https://github.com/zachsnoek/recurpy",
    author="Zachary D. Snoek",
    license="MIT",
    packages=["recurpy"],
    install_requires=required,
    entry_points={
        "console_scripts": [
            "recurpy=recurpy:main"
        ]
    },
    include_package_data=True
)