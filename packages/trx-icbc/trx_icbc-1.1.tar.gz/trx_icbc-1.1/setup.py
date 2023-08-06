# Copyright (c) 2020, Joaquin Pablo Tempelsman
# License: MIT
#   
import os
import pathlib
from setuptools import find_packages, setup

# EXTERNAL DATA



# SETUP #
setup(
    name="trx_icbc",
    version='1.01',
    author=["Tempelsman Joaquin, Miranda Chab"],
    author_email="jtempelsman@icbc.com.ar",
    description="transaction prediction models for access and mobile channels",
    license="MIT",
    install_requires=['pandas', 'numpy','logging','datetime' , 'typer','plotly', 'sphinx-rtd-theme'],


    #dependencias de prophet que no se terminan de instalar todas (lunar calendar tira error), instalar prophet y pystan por fuera.
    #['fbprophet','pystan','lunarcalendar', 'holidays' ,'convertdate', 'pymeeus', 'pyephem', 'korean-lunar-calendar']

    packages=find_packages()
   )


