from setuptools import setup, find_packages

long_description = 'Package that provides a CLI to interact with catfacts API' 

setup( 
    name='meowfacts',
    version='1.1.0',
    author='yadhu',
    author_email='yadhu621@gmail.com',
    url='https://github.com/yadhu621/meowfacts',
    description='Simple and Compound interest calculator',
    long_description= long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points ={ 
    'console_scripts': ['catty = meowfacts.cli:Cfcli'] 
    },
    keywords=['catfacts'],
    zip_safe=False,
    install_requires=[
        'requests',
        'PyYAML',
        'pandas==0.23.3',
        'numpy>=1.14.5'
    ]
)
