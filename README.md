# Lianjia Spider (Shanghai implemented)

Spider is designed to crawl renting houses on Lianjia site. which is based on scrapy and uses IPProxyPool as its proxy pool.

## Dependency

+ [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)

## Run

Clone this project and start IPProxyPool, then

```bash
cd lianjia_house/lianjia_house/spider
scrapy crawl lianjia_shanghai_house -o shanghai_houses.csv --loglevel INFO
```

## How to change city

If you want to crawl houses of another city, just do a copy and 

1\. Rename the files to your city.

2\. Replace "sh.lianjia.com" in `lianjia_{your city}_url.py` to the site of your city and re-run 

```bash
scrapy crawl lianjia_{your city}_url -o lianjia_{your city}_url.json --loglevel INFO
```

3\. Replace "lianjia\_shanghai\_url.json" in `lianjia_{your city}_house.py` to "lianjia\_{your city}\_url.json".


```bash
scrapy crawl lianjia_{your city}_house -o -o {your city}_houses.csv --loglevel INFO
```
## Update time

[TESTED] 2017.04.30
