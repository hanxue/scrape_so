import scrapy

class StackOverflowJobsRSS(scrapy.Spider):
    name = 'so_jobs_rss'
    start_urls = ['https://stackoverflow.com/jobs/feed?l=Remote&d=20&u=Miles'
    ]

    def parse(self, response):
        for result in response.css('item'):
            yield {
                'guid': result.css('guid::text').extract_first(),
                'company': result.css('a10\:name::text').extract_first(),
                'title': result.css('title::text').extract_first(),
                'category': result.css('category::text').extract(),
                'description': result.css('description::text').extract_first(),
                'published': result.css('pubDate::text').extract_first(),
                'updated': result.css('a10\:updated::text').extract_first(),
                'location': result.css('location::text').extract_first(),
                'url': result.css('link::text').extract_first(),
            }