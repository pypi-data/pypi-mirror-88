# CzechTVSrtScraper
Scraper of hidden subtitles from Czech TV pages into SRT format.

## Usage

To create SRT file with subtitles scraped from the webpage type following

```python
# first episode of Most! series
url = 'https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010001/titulky'

# scrape and save
import CzechTVSrt as CTsrt
CTsrt.scrape_srt(url, 'output.srt')
```

By default `requests` library is used for fetching. In order to use `Selenium`, it needs to be installed separately (manually) as well as the browser driver. By default, Chrome is used.

To use `Selenium`, type

```python
import CzechTVSrt as CTsrt
CTsrt.scrape_srt(url, 'output.srt', use_selenium = True)
```

To use `Selenium` and `Firefox` as the browser type

```python
import CzechTVSrt as CTsrt
CTsrt.scrape_srt(url, 'output.srt', use_selenium = True, browser = 'firefox')
```

The subtitles have specified only the start point, so the threshold for length can be set so it is well timed, by default it is `10 s`. Set the threshold in seconds with

```python
import CzechTVSrt as CTsrt
CTsrt.scrape_srt(url, 'output.srt', max_duration = 7)
```

## Contribution

Author: **Martin Benes**

