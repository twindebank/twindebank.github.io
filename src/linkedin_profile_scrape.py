import os

from scrape_linkedin import Scraper

LI_AT = os.getenv('LI_AT')

with Scraper(cookie=LI_AT) as scraper:
    profile_info = scraper.get_profile('http://www.linkedin.com/in/theowindebank').to_dict()
    print(profile_info)
