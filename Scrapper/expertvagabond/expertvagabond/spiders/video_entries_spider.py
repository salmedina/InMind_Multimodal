import scrapy
from bs4 import BeautifulSoup
from bs4.element import NavigableString

class VideoEntriesSpider(scrapy.Spider):
    name = 'videoentries'

    def start_requests(self):
        urls=['https://expertvagabond.com/travel-video/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for entry in response.css('h2.entry-title a'):
            # Here we can call the blog post parse
            yield scrapy.Request(entry.css('a::attr(href)').extract()[0], callback=self.parse_blog_entry)

        next_page = response.css('div.nav-previous a::attr(href)').extract()
        print next_page
        if len(next_page) > 0:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_blog_entry(self, response):
        # TITLE
        title = response.css('h1.entry-title span::text').extract()[0].strip()

        # ENTRY
        entry = response.css('div.entry-content')

        # IMAGE LIST
        image_list = []
        for x in entry.css('img'):
            try:
                image_list.append({'caption':x.css('img::attr(title)').extract_first(), 'url':x.css('img::attr(src)').extract_first()} )
            except:
                print '>>>', title, '<<<'
                print '>>>', response.url, '<<<'


        # VIDEO
        video = entry.css('iframe::attr(src)').extract()[-1]
        video = video.replace('www.youtube.com/embed/', 'www.youtube.com/watch?v=')

        # TEXT
        # Gather the text from the page
        soup = BeautifulSoup(entry.extract()[0])
        tagged_text = []
        for child in soup.recursiveChildGenerator():
            if type(child) is NavigableString:
                tagged_text.append((child.parent.name, child))
        # Compress into titles and paragraphs while cleaning out the empty entries
        compressed_text =[]
        acc_str = u''
        for item in tagged_text:
            if item[0] == 'div':
                if len(acc_str) > 0:
                    compressed_text.append(('p', acc_str))
                    acc_str = u''
            elif item[0] in ['h1','h2','h3','h4','h5']:
                if len(acc_str) > 0:
                    compressed_text.append(acc_str)
                    acc_str = u''
                compressed_text.append(item)
            elif len(item[1]) > 0:
                acc_str += item[1]

        yield {
            'entry_url' : response.url,
            'title' : title,
            'images' : image_list,
            'video_url': video,
            'text' : compressed_text
        }
