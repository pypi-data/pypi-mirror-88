import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='WestCoastAD',
      version='1.0',
      packages= setuptools.find_packages(),
      author="Anita Mahinpei, Yingchen Liu, Erik Adames, Lekshmi Santhosh",
      description="An Optimization Package with an Automatic Differenation Core",
      long_description= long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/West-Coast-Differentiators/cs107-FinalProject",
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      install_requires = [ 'numpy==1.19.3' ]
)