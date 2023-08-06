import setuptools

with open('README.md', 'r') as wf:
    long_description = wf.read()

setuptools.setup(
    name="busie-consumer",
    version="1.0.0",
    author="Brady Perry",
    author_email="brady@getbusie.com",
    description="Base Kafka Consumer for Busie Projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bradyperry@bitbucket.org/busie/busie-consumer.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    install_requires=[
        "confluent_kafka",
    ]
)
