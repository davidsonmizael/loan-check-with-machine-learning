from setuptools import setup, find_packages

requirements = open('requirements.txt','r').read()

setup(
    name="Credit Analysis with Face Recognition",
    version="1.0.0",
    description="This project was made to determine if a person is eligible for a loan or not using face recognition during its appliance",
    python_requires='!=3.7',
    packages=find_packages(),
    install_requires=requirements,
    test_suite='tests',
    tests_require=[
        'pytest'
    ]
)