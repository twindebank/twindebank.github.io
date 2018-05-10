import json
import os

from dominate.tags import body, section, p, div, article, i, span

from src.patched_scraper import PatchedScraper


def scrape_profile(cookie):
    with PatchedScraper(cookie=cookie) as scraper:
        profile_info = scraper.get_profile('http://www.linkedin.com/in/theowindebank').to_dict()
        return replace_none_with_str_recurs(profile_info)


def profile_to_html(profile_info):
    html_body = body()
    with html_body:
        with section(_class="leading animated fadeInDown"):
            p(profile_info['personal_info']['name'], _class="leading-bigtext")
            p(profile_info['personal_info']['summary'], _class="leading-text")
        for section_title, roles in profile_info['experiences'].items():
            with section(_class="cards animated fadeInUp"):
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
                                        div(role['location'], _class='entry-location')
                                    div(role['description'], _class="entry-body")
                                elif section_title == "education":
                                    with div(_class='entry-header'):
                                        div(role['field_of_study'], _class='entry-title')
                                        div(role['date_range'], _class='entry-date')
                                    with div(_class="entry-subheader"):
                                        div(role['name'], _class='entry-organisation')
                                        with div(_class='entry-location'):
                                                span(role['degree'])
                                                if role['grades'] != '':
                                                    i(f", {role['grades']}", style="font-weight:300")
                                    div(role['description'], _class="entry-body")

    return str(html_body)


def save_html(html, filename):
    cv_body_file = open(filename, "w")
    cv_body_file.write(html)
    cv_body_file.close()


def replace_none_with_str_recurs(any_dict):
    for k, v in any_dict.items():
        if v is None:
            any_dict[k] = ""
        elif isinstance(v, dict):
            replace_none_with_str_recurs(v)
        elif isinstance(v, list):
            for n, item in enumerate(v):
                if isinstance(item, dict):
                    replace_none_with_str_recurs(item)



def main():
    # LI_AT = os.getenv('LI_AT')
    # profile_info = scrape_profile(LI_AT)
    profile_info = json.load(open('profile.json'))
    html = profile_to_html(profile_info)
    save_html(html, "cv-body.html")


if __name__ == '__main__':
    main()
