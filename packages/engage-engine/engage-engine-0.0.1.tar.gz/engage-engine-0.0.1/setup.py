import setuptools

# Reads README.md and sets it to long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="engage-engine", # Replace with package name
    version="0.0.1", # Change for every update
    author="BD103", # Your name / username
    author_email="dont@stalk.me", # YEmail
    description="The Engage Engine", # Small Desc
    long_description=long_description, # Keep
    long_description_content_type="text/markdown", # Keep
    url="https://github.com/Team-Engage/engine", # Github / Repl.it / Website URL
    packages=setuptools.find_packages(), # DO NOT EDIT
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Edit based on https://pypi.org/classifiers/
    python_requires='>=3.6', # Don't change unless you know what you're doing
)