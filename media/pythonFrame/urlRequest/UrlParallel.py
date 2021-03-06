from pythonFrame.urlRequest.UrlBase import JsonBase
from pythonFrame.myUtils.Util import Util


__author__ = 'linzhou208438'


class JsonParallel(JsonBase):
    def __init__(self, monitor, cpu=8):
        JsonBase.__init__(self, monitor, cpu)

    def url_append(self):
        for vid in self.monitor.vids:
            self.format_urls.append(self.url % vid)



    def monitor_exception_count(self, e, isTimeout_retry, url):
        if str(e).find('urlopen error timed out') > -1:
            if not isTimeout_retry:
                self.monitor.urls_parallel_timeout.append(url)
            else:
                self.monitor.urls_retry_failure.append(url)
        Util.printf('urlopen-->%s | exception--> %s' % (url, e))


    def monitor_url_count(self, isTimeout, url):
        if not isTimeout:
            self.monitor.urls_parallel_running.append(0)

    def monitor_urls_len(self,urls):
        self.monitor.urls_parallel_total = len(self.format_urls)

    def retry_timeout(self):
        for url2 in self.monitor.urls_parallel_timeout:
            self.json_run(url2, True)
            self.monitor.urls_parallel_timeout_retry.append(url2)
