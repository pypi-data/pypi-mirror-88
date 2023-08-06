from setuptools import setup
import pathlib

plugin_dir = pathlib.Path(__file__).parent.absolute()

with open(f"{plugin_dir}/README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Tenzir",
    author_email="engineering@tenzir.com",
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Software Development :: Object Brokering",
    ],
    description="A RabbitMQ backbone for threatbus.",
    entry_points={"threatbus.backbone": ["rabbitmq = threatbus_rabbitmq.plugin"]},
    install_requires=["threatbus>=2020.12.16", "pika>=1.1.0", "retry"],
    keywords=["threatbus", "plugin"],
    license="BSD 3-clause",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="threatbus-rabbitmq",
    packages=["threatbus_rabbitmq"],
    python_requires=">=3.7",
    url="https://github.com/tenzir/threatbus",
    version="2020.12.16",
)
