from setuptools import setup, find_packages

setup(
    name='bbc_food_scraper',
    version='0.1.0',
    description='pulling recipe data from bbc',
    author='Ben Farrell',
    author_email='ben.farrell08@gmail.com',
    packages=find_packages(include=['bbc_food_scraper', 'bbc_food_scraper.*']),
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'certifi',
        'charset-normalizer',
        'idna',
        'requests',
        'soupsieve',
        'urllib3',
    ],
    setup_requires=['flake8'],
    tests_require=['pytest'],
)