from setuptools import setup


name: str = "sourceRank"
version: str = "2.0.2"
license: str = "MIT"
author: str = "David Martin-Gutierrez"
author_email: str = "dmargutierrez@gmail.com"

setup(name=name,
      version=version,
      packages=[name],
      license=license,
      author=author,
      author_email=author_email,
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"],
      package_dir={name: name},
      package_data={
        name: ['resources/resources_domains.csv']},
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=['requests',
                        'tldextract==3.1.0',
                        'tweepy','newsapi-python',
                        'numpy',
                        'GetOldTweets3',
                        'coloredlogs',
                        'fuzzywuzzy',
                        'scipy',
                        'pycountry',
                        'python-dateutil',
                        'pandas',
                        'aiodns',
                        'aiohttp-socks',
                        'aiohttp',
                        'cchardet',
                        'elasticsearch',
                        'fake-useragent',
                        'geopy',
                        'googletransx',
                        'schedule',
                        'googlesearch-python',
                        'python-restcountries',
                        'twine',
                        'bumpversion',
                        'botometer',
                        'dataclasses',
                        'langdetect',
                        'more_itertools',
                        'python-Levenshtein',
                        'twint'])