# Scrapy settings for bayscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bayscraper'

SPIDER_MODULES = ['bayscraper.spiders']
NEWSPIDER_MODULE = 'bayscraper.spiders'
ITEM_PIPELINES = {}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'zozor (+http://www.idonthaveadomain.com)'
