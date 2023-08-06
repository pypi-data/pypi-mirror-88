import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demand-manager", # Replace with your own username
    version="0.0.1",
    author="Shan Dora He",
    author_email="dora.shan.he@gmail.com",
    description="Demand manager is an optimisation package for scheduling loads of households,"
                " including electric appliances, batteries and EV. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dorahee/demand-manager.git",
    packages=setuptools.find_packages(include=['demand-manager', 'demand-manager.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)