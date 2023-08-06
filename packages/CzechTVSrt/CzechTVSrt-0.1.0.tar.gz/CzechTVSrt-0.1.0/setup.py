
# requirements
try:
  with open('requirements.txt') as f:
    reqs = f.read().splitlines()
except:
  reqs = []

import setuptools
with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'CzechTVSrt',
  version = '0.1.0',
  author = 'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Scraper for Czech TV subtitles.',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='MIT',
  url = 'https://github.com/martinbenes1996/CzechTVSrt',
  download_url = 'https://github.com/martinbenes1996/CzechTVSrt/archive/0.1.0.tar.gz',
  keywords = ['subtitles', 'titulky', 'srt', 'czechia', 'scraping', 'webscraping', 'ivysilani'],
  install_requires=reqs,
  package_dir={'': '.'},
  package_data={'': ['data/*.json','data/*.csv']},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Other Audience',
    'Natural Language :: Czech',
    'Topic :: Internet',
    'Topic :: Multimedia',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Video',
    'Topic :: Text Processing :: Markup :: HTML',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)