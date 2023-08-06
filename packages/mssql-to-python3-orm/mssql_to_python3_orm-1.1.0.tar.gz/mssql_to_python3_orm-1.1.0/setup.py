import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mssql_to_python3_orm",
    version="1.1.0", # UPDATE README IN LAB3!!!
    description="MS SQL Server to Python 3 ORM",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Maiia Chudinova, Valeriia Yaroshenko, Dmitry Shvab",
    url="https://github.com/MaiiaChudinova/univ_metaprogramming",
    packages=["mssql_to_python3_orm"],
    entry_points={
        "console_scripts": ['mssql_to_python3_orm = mssql_to_python3_orm.main:main']
    },
    install_requires=["pyodbc"]
)