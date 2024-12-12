#!/bin/bash

python -m conf_crawler.crawl && \
python -m conf_crawler.postprocess && \
python -m conf_crawler.filter && \
python -m conf_crawler.visualize