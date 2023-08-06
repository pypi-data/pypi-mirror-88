from setuptools import setup, find_packages
setup(
    name="cmdog",
    version="0.0.1",
    description="Monitor process operation",
    author="Jannchie",
    author_email="jannchie@gmail.com",
    packages=find_packages(),
    platforms="any",
    install_requires=["docopt"],
    entry_points={
        "console_scripts": ['cmdog = pkg.watchdog:cmd']
    }
)
