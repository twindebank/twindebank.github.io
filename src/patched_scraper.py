import scrape_linkedin
from scrape_linkedin import Scraper, Profile


def get_school_info(school):
    return scrape_linkedin.get_info(school, {
        'name': '.pv-entity__school-name',
        'degree': '.pv-entity__degree-name span:nth-of-type(2)',
        'grades': '.pv-entity__grade span:nth-of-type(2)',
        'field_of_study': '.pv-entity__fos span:nth-of-type(2)',
        'date_range': '.pv-entity__dates span:nth-of-type(2)',
        'activities': '.activities-societies',
        'description': '.pv-entity__description'
    })


class PatchedProfile(Profile):
    @property
    def experiences(self):
        """
        Returns:
            dict of person's professional experiences.  These include:
                - Jobs
                - Education
                - Volunteer Experiences
        """
        experiences = {}
        container = scrape_linkedin.one_or_default(self.soup, '.background-section')

        jobs = scrape_linkedin.all_or_default(container, '#experience-section ul > li')
        jobs = list(map(scrape_linkedin.get_job_info, jobs))
        experiences['jobs'] = jobs

        schools = scrape_linkedin.all_or_default(container, '#education-section ul > li')
        schools = list(map(get_school_info, schools))
        experiences['education'] = schools

        volunteering = scrape_linkedin.all_or_default(
            container, '.pv-profile-section.volunteering-section ul > li')
        volunteering = list(map(scrape_linkedin.get_volunteer_info, volunteering))
        experiences['volunteering'] = volunteering

        return experiences


class PatchedScraper(Scraper):
    def get_profile(self, url):
        self.load_profile_page(url)
        profile = self.driver.find_element_by_id(
            'profile-wrapper').get_attribute("outerHTML")
        return PatchedProfile(profile)
