from setuptools import setup

setup(name='basis_reduction',
      version='1.1.1',
      author='Artur Buriev',
      author_email="arturburiev@yandex.com",
      description='Python3 implementation of LLL and Gaussian method',
      license="MIT",
      url="https://github.com/arturburiev/basis_reduction",
      packages= ['basis_reduction'],
      install_requires=[
          'numpy',
      ],
	  classifiers=[
	        "Development Status :: 3 - Alpha",
	        "License :: OSI Approved :: MIT License",
	        "Programming Language :: Python :: 3.6",
	        "Programming Language :: Python :: 3.7",
	        "Programming Language :: Python :: 3.8",
	        "Programming Language :: Python :: 3 :: Only",
	    ],
)