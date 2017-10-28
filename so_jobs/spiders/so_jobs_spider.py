import scrapy
from so_jobs.items import ModelItem
from so_jobs.pipelines import StackJob

class StackOverflowJobsSpider(scrapy.Spider):
    name = 'so_jobs'
    start_urls = ['https://stackoverflow.com/jobs?l=Remote&d=20&u=Miles&sort=p'
    ]

    def parse(self, response):
        for result in response.css('.-job-item'):
            # job = StackJob()
            # job = ModelItem(StackJob())
            job = ModelItem(StackJob())
            job['company'] = result.css('.-company .-name::text').extract_first()
            job['title'] = result.css('.job-link::text').extract_first()
            job['location'] = result.css('.-company .-location::text').extract_first()
            job['perks'] = result.css('.-perks span::text').extract()
            job['url'] = result.css('.job-link::attr(href)').extract_first()
            yield job
        
        next_page = response.css('.pagination .test-pagination-next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)