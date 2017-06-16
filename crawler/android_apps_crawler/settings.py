# Scrapy settings for android_apps_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'android_apps_crawler'

SPIDER_MODULES = ['android_apps_crawler.spiders']
NEWSPIDER_MODULE = 'android_apps_crawler.spiders'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11(KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
        'android_apps_crawler.pipelines.AppPipeline' : 1,
}
MONGODB_HOST= '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME= 'GPLAY'
MONGODB_DOCNAME= 'Apps'

LOG_LEVEL = 'DEBUG'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
    #CONCURRENT_REQUESTS_PER_DOMAIN = 16
    #CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'myFirstCrawler.middlewares.MyfirstcrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'myFirstCrawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# DOWNLOADER_MIDDLEWARES = {
#     'android_apps_crawler.middlewares.DownloaderMiddleware': 1,
# }

# Uncomment following statement to use proxy.
# PROXIES = {
#     'http' : '',
# }

# only crawl down to the 3rd level
DEPTH_LIMITS = 2;

ALLOWED_DOMAINS = {
    "appchina.com" : ["appchina.com",],
    "hiapk.com"    : ["apk.hiapk.com",],
    "anzhi.com"    : ["anzhi.com",],
    "android.d.cn" : ["android.d.cn",],
    "mumayi.com"   : ["mumayi.com",],
    "gfan.com"     : ["apk.gfan.com",],
    "nduoa.com"    : ["nduoa.com",],
    "3gyu.com"     : ["3gyu.com",],
    "angeeks.com"  : ["angeeks.com",],
    "appfun.cn"    : ["appfun.cn",],
    "jimi168.com"  : ["jimi168.com",],
    "7723.com"     : ["7723.com",],
    "777ccc.com"   : ["777ccc.com",],
    "anruan.com"   : ["anruan.com",],
}
START_URLS = {
    "appchina.com" : ["http://www.appchina.com",],
    "hiapk.com"    : ["http://apk.hiapk.com",],
    "anzhi.com"    : ["http://www.anzhi.com",],
    "android.d.cn" : ["http://android.d.cn",],
    "mumayi.com"   : ["http://www.mumayi.com",],
    "gfan.com"     : ["http://apk.gfan.com",],
    "nduoa.com"    : ["http://www.nduoa.com",],
    "3gyu.com"     : ["http://www.3gyu.com",],
    "angeeks.com"  : ["http://www.angeeks.com",],
    "appfun.cn"    : ["http://www.appfun.cn",],
    "jimi168.com"  : ["http://www.jimi168.com/",],
    "7723.com"     : ["http://www.7723.com",],
    "777ccc.com"   : ["http://www.777ccc.com",],
    "anruan.com"   : ["http://www.anruan.com",],
}
SCRAPE_RULES = {
    "xpath" : {
        "appchina"     : "//a[@class='download-pc fl']/@href",
        "hiapk"        : "//a[@id='appInfoDownUrl']/@href",
        "android.d.cn" : "//a[@class='localDownload']/@href",
        "mumayi"       : "//a[@class='download fl']/@href",
        "gfan"         : "//a[@id='computerLoad']/@href",
        "nduoa"        : "//a[@class='d_pc_normal']/@href",
        "3gyu"         : "//a[@class='ldownload']/@href",
        "angeeks"      : "//div[@class='rgmainsrimg'][1]/a/@href",
        "appfun"       : "//a[@class='downcp']/@href",
        "jimi168"      : "//a[@class='a_sign2']/@href",
        "7723"         : "//ul[@class='download_list']/li/h5/a/@href",
        "777ccc"       : "//a[@class='downtopc']/@href",
        "anruan"       : "//a[@class='ldownload']/@href",
    },
    "custom_parser" : {
        "anzhi" : "parse_anzhi",
    },
}
CRAWL_RULES = {
    "hiapk.com"    : ["http://apk\.hiapk\.com/appinfo",],
}
DATABASE_DIR = "../repo/databases/"
MARKET_NAME = ""
