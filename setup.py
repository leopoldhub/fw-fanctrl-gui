from distutils.core import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("requirements.txt", "r") as f:
    devRequirements = f.read().splitlines()

setup(
    name="fw-fanctrl-gui",
    version="0.0.1",
    packages=["src"],
    install_requires=requirements,
    extras_require={"dev": devRequirements},
    url="https://github.com/leopoldhub/fw-fanctrl-gui",
    license="BSD-3-Clause",
    author="leopoldhub",
    author_email="hubertleopold01@gmail.com",
    description="Simple tkinter python gui for fw-fanctrl.\nA separate installation of fw-fanctrl is required.",
    entry_points={"console_scripts": ["fw-fanctrl-gui=src.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
