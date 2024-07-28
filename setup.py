from setuptools import setup, find_packages



def get_requirements(file_name: str) -> list[str]:

    with open(file_name) as file:
        package_list = file.readlines()
        HYPENDOT = '-e .'
        packages = [package.strip().replace('\n', '')  for package in package_list if package.strip() != HYPENDOT]
       
        return packages



setup(
    name = 'flight_fare_prediction',
    version = '0.0.1',
    author = 'Nagarjun R',
    author_email = 'nagarjunramakrishnan10@gmail.com',
    description = "A project for flight fare prediction",
    packages = find_packages(where='src'),
    package_dir = {'':'src'},
    install_requires = get_requirements(file_name='requirements.txt')
    
)
