@echo off
if "%1"=="" (
    ECHO "Usage: %0 <market name> [database output directory]"
    ECHO "   market name:"
    ECHO "       appchina.com"
    ECHO "       hiapk.com"
    ECHO "       anzhi.com"
    ECHO "       android.d.cn"
    ECHO "       mumayi.com "
    ECHO "       gfan.com"
    ECHO "       nduoa.com"
    ECHO "       3gyu.com"
    ECHO "       angeeks.com"
    ECHO "       appfun.cn"
    ECHO "       jimi168.com"
    ECHO "   database output directory:"
    ECHO "       default: ../repo/databases/"
    exit 2
    )

if "%2"=="" (
    scrapy crawl android_apps_spider -s JOBDIR=job_%1 -a market=%1
    ) else (
    scrapy crawl android_apps_spider -s JOBDIR=job_%1 -a market=%1 -a database_dir=%2
    )
