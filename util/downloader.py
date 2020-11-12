from util.Log import get_logger
from fake_useragent import UserAgent
import requests
import time
import datetime


class Downloader:
    logger = get_logger(__name__)

    def __init__(self, url, delay=5, user_agent=r"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
                 num_retries=0):
        """

        :param delay:
        :param user_agent:默认使用随机ua
        :param prxies:
        :param num_retries:
        :param cache:
        """
        self.throttle = Throttle(delay)
        self.user_agent = UserAgent()
        self.num_retries = num_retries
        self.url = url

    def __call__(self):
        return self.dow(self.url)

    def dow(self, url):
        result = self.download(url=url, headers={"User-Agent": self.user_agent.random}, num_retries=self.num_retries)
        return result

    def download(self, url, headers, num_retries):
        self.logger.info("Downloading: " + url)
        try:
            req = requests.get(url, headers=headers)
            html = req.text
            if 500 <= req.status_code < 600:
                # 服务器错误则忽略缓存并重新下载
                time.sleep(2)
                html = requests.get(url, headers=headers).text
                if 500 <= req.status_code < 600:
                    html = ""
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code <= 600:
                    html = self.download(url=url, headers=headers, num_retries=num_retries - 1)
        # if html is None:
        #     self.throttle.wait(url)
        #     html = self.download(url=url, headers=headers, num_retries=num_retries)
        return html


class Throttle:
    """
    在下同一域名时增加下载延迟
    """

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = requests.utils.urlparse(url)
        last_acessed = self.domains.get(domain)

        if self.delay > 0 and last_acessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_acessed).seconds
            if sleep_secs > 0:
                # 该domain刚访问过，因此需要休眠
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()


if __name__ == '__main__':
    print(Downloader('http://aan.how/browse/paper/30000')())
