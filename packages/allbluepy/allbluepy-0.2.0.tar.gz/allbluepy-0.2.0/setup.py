from setuptools import setup, find_packages

setup(name='allbluepy',
    version='0.2.0',
    url='https://github.com/BSFernando',
    license='MIT License',
    description='Informações oceânicas referente a região mais próxima as cordenadas de entrada',
    author='Fernando Borges',
    author_email='bs_fernando@hotmail.com',
    keywords='packages',
    packages=['allbluepy'],
    include_package_data=True,
    install_requires=['pandas'])
