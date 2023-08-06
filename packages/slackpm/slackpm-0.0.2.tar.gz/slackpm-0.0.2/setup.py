import setuptools

setuptools.setup(
    name="slackpm",  # Replace with your own username
    version="0.0.2",
    author="Arnab Mukherjee",
    author_email="mukherjeearnab.arc@gmail.com",
    description="This is a simple script to send push message to Slack channels using Webhooks URL with Slack Apps.",
    long_description=open("README.md").read() + '\n\n' + \
    open("CHANGELOG.txt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mukherjeearnab/slackpm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
