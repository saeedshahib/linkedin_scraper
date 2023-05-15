import scrapy


class LinkedInSpider(scrapy.Spider):
    name = "linkedin_spider"
    allowed_domains = ["linkedin.com", "zoominfo.com"]

    def start_requests(self):
        # Provide your LinkedIn Sales Navigator search URL here
        search_url = "Your linkedin sales navigator search url"
        yield scrapy.Request(search_url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        # Extract the link to the desired profile
        profile_link = response.css(".search-result__info .search-result__result-link::attr(href)").get()
        yield response.follow(profile_link, callback=self.parse_profile)

    def parse_profile(self, response):
        # Extract the name and company from the profile page
        name = response.css(".profile-topcard-person-entity__name span::text").get()
        company = response.css(".profile-topcard-person-entity__company span::text").get()

        # Extract the profile link from ZoomInfo (assuming it's available on the page)
        zoominfo_link = response.css(".profile-topcard__contact-info .ci-email a::attr(href)").get()
        yield response.follow(zoominfo_link, callback=self.parse_zoominfo, meta={'name': name, 'company': company})

    def parse_zoominfo(self, response):
        name = response.meta.get('name')
        company = response.meta.get('company')
        # Extract the phone number from the ZoomInfo page
        phone_number = response.css(".contact-info__phone .ci-data::text").get()
        yield {
            'name': name,
            'company': company,
            'phone_number': phone_number
        }

    def parse(self, response, **kwargs):
        pass
