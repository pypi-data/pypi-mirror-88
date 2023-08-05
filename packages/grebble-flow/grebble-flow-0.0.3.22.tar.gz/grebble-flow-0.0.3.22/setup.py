import os
from distutils.command.install import install
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()


class custom_install(install):
    def run(self):
        install.run(self)
        from grebble_flow.grpc.commands import install_proto
        install_proto()


setup(
    name="grebble-flow",
    version="0.0.3.22",
    packages=find_packages(exclude=("tests", "example")),
    description="Grebble flow",
    long_description=README,
    author="Greble",
    author_email="info@grebble.io",
    url="https://github.com/Grebble-team/python-flow-helper",
    install_requires=["click", "grpcio", "grpcio-tools", "docstring_parser==0.7.3", "dataclasses-serialization==1.3.1"],
    cmdclass={
        'install': custom_install,
    },
)
