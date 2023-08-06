
# html
import requests
from bs4 import BeautifulSoup
# datetime
from datetime import datetime, timedelta

class CzechTV_SRT:
    """Scraper for subtitles from Czech TV ivysilani page.
    
    The fetching of the page is done with requests, but Selenium is supported as well.
    Selenium and browser driver need to be installed separately manually before.
    """
    def __init__(self, use_selenium = False, browser = "chrome"):
        """Constructor.
        
        Args:
            use_selenium (bool, optional): Enables Selenium if True. If False, requests is used.
            browser (str, optional): Selects browser for Selenium. Options {"chrome","firefox"}.
                                     Chrome by default.
        """
        self._selenium = use_selenium
        self._browser = browser
    
    def scrape(self, url, output = None, max_duration = 10):
        """Scrape the subtitles and save.
        
        Args:
            url (str): URL of the source page. Should start https://www.ceskatelevize.cz/ivysilani/...
            output (str, optional): Output file path. If not given, no output.
            max_duration (int, optional): Max seconds of single subtitle line on screen.
                                          By default 10s.
        """
        # get srt from html
        self._html = self._get_html(url)
        self._srt = self._parse_html(self._html, max_duration)
        # save the result
        if output:
            self._write_srt(self._srt, output)
        return self
    
    def _get_html(self, url):
        """Get HTML of given URL, either using selenium, or with requests."""
        if self._selenium:
            from selenium import webdriver
            if self._browser.lower() == "chrome":
                self._driver = webdriver.Chrome()
            elif self._browser.lower() == "firefox":
                self._driver = webdriver.Firefox()
            else: raise RuntimeError("browser %s not supported" % (self._browser))
            self._driver.get(url)
            return self._driver.page_source
        else:
            return requests.get(url).text
    def _parse_html(self, html, max_duration):
        """Parse given HTML with BeautifulSoup."""
        # get content
        soup = BeautifulSoup(html, features="html.parser")
        
        # parse html
        srt = []
        subtitle_lines = soup.select('#subtitles > div > ul > li')
        for i,line in enumerate(subtitle_lines):
    
            # text
            txt_list = line.get_text().strip().split("\n")
            text = '\n'.join(txt_list[1:])
    
            # time
            ms = int(line.select("li > a")[0]['rel'][0])
            tm = '%02d:%02d:%02d,%03d' % (ms // 3600000,           # h
                                          (ms % 3600000) // 60000, # min
                                          (ms % 60000) // 1000,    # sec
                                          ms % 1000)               # ms
            # prev end
            if srt:
                # parse times
                prev_start = self._time(srt[-1]['start'])
                curr_start = self._time(tm)
                # saturate subtitle
                prev_end = prev_start + min(curr_start - prev_start, timedelta(seconds = max_duration))
                srt[-1]['end'] = self._format_time(prev_end)

            # append    
            srt.append({
                # timing
                'start': tm,
                'end': None,
                # content
                'text': text
            })

        # final time
        prev_start = self._time(srt[-1]['start'])
        srt[-1]['end'] = self._format_time(prev_start + timedelta(seconds = max_duration))
        
        return srt

    # write srt
    def _write_srt(self, srt, output):
        """Output the srt object into output in SRT format."""
        with open(output, "w", encoding = "UTF-8") as fp:
            for i,sb in enumerate(srt):
                fp.write(str(i + 1) + "\n")
                fp.write(sb['start'] + ' --> ' + sb['end'] + "\n")
                fp.write(sb['text'] + "\n")
                if 'text_tr' in sb:
                    fp.write(sb['text_tr'] + "\n")
                fp.write('\n')
    @staticmethod
    def _time(dt):
        """Parse time into datetime object."""
        return datetime.strptime(dt, "%H:%M:%S,%f")
    @staticmethod
    def _format_time(dt):
        """Format datetime object into SRT time format."""
        return datetime.strftime(dt, "%H:%M:%S,%f")[:-3]

def scrape_srt(url, output, max_duration = 6, use_selenium = False, browser = "chrome"):
    """Shortcut function for subtitle scraping of Czech TV.
    
    Args:
        url (str): URL of the page. Should start https://www.ceskatelevize.cz/ivysilani/...
        output (str): Output file path.
        max_duration (int, optional): Max duration of single subtitle line.
        use_selenium (bool, optional): Switch between requests (False) and selenium (True).
        browser (str, optional): Choice of browser for selenium ("chrome","firefox"), chrome by default.
    Returns:
        None. Saves the subtitles into output file (side effect).
    """
    CzechTV_SRT(use_selenium = use_selenium, browser = browser)\
        .scrape(url = url, output = output, max_duration = max_duration)

if __name__ == "__main__":
    # get srt
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010001/titulky"
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010002/titulky"
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010003/titulky"
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010004/titulky"
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010005/titulky"
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010006/titulky"
    #url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010007/titulky"
    url = "https://www.ceskatelevize.cz/ivysilani/10995220806-most/216512120010008/titulky"
    
    scrape_srt(url, "most_8_requests.srt", max_duration = 6)

__all__ = ["CzechTV_SRT", "scrape_srt"]