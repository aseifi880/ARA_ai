#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard libraries
from abc import ABC

# local-application libraries
from scrapers import BaseScraper


class JobyabiScraper(BaseScraper, ABC):
    base_url = "https://jobyabi.com"

    def __init__(self):
        super().__init__()




