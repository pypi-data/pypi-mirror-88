import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='zcross',  
     version='0.0.4',
     scripts=[] ,
     author="Michele Renda",
     author_email="michele.renda@cern.ch",
     description="An utility to read low-pressure gaseous cross sections data",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://gitlab.com/micrenda/zcross-python",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.0',
     entry_points = {
        'console_scripts': ['zcross-xml=zcross.zcross_xml:main'],
    }
 )
