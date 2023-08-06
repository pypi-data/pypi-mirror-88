import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syslog-py",
    version="0.2.2",
    author="Maciej Budzyński",
    author_email="maciej.budzyn@gmail.com",
    description="Syslog client implementation (RFC 3164/RFC 5424) with message transfer from RFC 6587 (Syslog over TCP)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maciejbudzyn/syslog-py",
    packages=setuptools.find_packages(),
    classifiers=[
	'Development Status :: 3 - Alpha',
    "Programming Language :: Python :: 3",
	'Operating System :: Unix',
	'Operating System :: POSIX :: Linux',
	'Operating System :: Microsoft',
    ],
    python_requires='>=3.5',
    keywords='syslog logging octet-counting octet-stuffing',
    
)
