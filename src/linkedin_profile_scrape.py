import json
import os

from dominate.tags import body, section, p, div, article
from scrape_linkedin import Scraper


def scrape_profile(cookie):
    with Scraper(cookie=cookie) as scraper:
        profile_info = scraper.get_profile('http://www.linkedin.com/in/theowindebank').to_dict()
        return profile_info


def profile_to_html(profile_info):
    html_body = body()
    with html_body:
        with _main():
        with section(_class="leading animated fadeInDown"):
            p(profile_info['personal_info']['name'], _class="leading-bigtext")
            p(profile_info['personal_info']['summary'], _class="leading-bigtext")
        with section(_class="cards animated fadeInUp"):
            for section_title, roles in profile_info['experiences'].items():
                div(section_title, _class='section-title')
                for role in roles:
                    if len(set(role.values())) > 1:
                        with article():
                            with div(_class='cventry'):
                                if section_title == "jobs":
                                    with div(_class='entry-header'):
                                        div(role['title'], _class='entry-title')
                                        div(role['date_range'], _class='entry-date')
                                    with div(_class="entry-subheader"):
                                        div(role['company'], _class='entry-organisation')
                                        if role['location']:
                                            div(role['location'], _class='entry-location')
                                    div(role['description'], _class="entry-body")
                                elif section_title == "education":
                                    with div(_class='entry-header'):
                                        if role['field_of_study']:
                                            div(role['field_of_study'], _class='entry-title')
                                        div(role['date_range'], _class='entry-date')
                                    with div(_class="entry-subheader"):
                                        div(role['name'], _class='entry-organisation')
                                        div(f"{role['degree']} <i>{role['grades']}</i>", _class='entry-location')
    return str(body)


def save_html(html, filename):
    cv_body_file = open(filename, "w")
    cv_body_file.write(html)
    cv_body_file.close()


def main():
    # LI_AT = os.getenv('LI_AT')
    # profile_info = scrape_profile(LI_AT)
    profile_info = json.load(open('profile.json'))
    html = profile_to_html(profile_info)
    save_html(html, "cv-body.html")


if __name__ == '__main__':
    main()
