import asyncio
import json
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
import os
from crawlee import ConcurrencySettings

async def main() -> None:
    concurrency_settings = ConcurrencySettings(
        # Set the maximum number of concurrent requests the crawler can run to 10.
        max_concurrency=20,
    )


    def sanitize_filename(url: str) -> str:
        #if url.startswith('http://'):
        #    url = url.removeprefix('http://')
        #elif url.startswith('https://'):
        #    url = url.removeprefix('https://')
        return url.replace('/', '+').replace(':','+')

    # Initialize crawler
    crawler = BeautifulSoupCrawler(max_crawl_depth=2, max_requests_per_crawl=20, concurrency_settings = concurrency_settings)
    data = {}

    # Load seed URLs
    with open('undergraduates/undergraduates2.json', 'r', encoding='utf-8-sig') as f:
        degrees_json = json.load(f)
        urls = [item['department_url'] for item in degrees_json]

    track_urls = [{'url': url, "userData": {"origin_seed": url}} for url in urls]

    @crawler.router.default_handler
    async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
        url = context.request.url
        if url in urls:
            origin_url = url
        else:
            origin_url = context.request.label
        # Skip URLs containing '/en/'
        #if '/en/' in url:
        #    url.replace('/en/', '/el/')
        #    return

        # Extract page data
        title = context.soup.title.string.strip() if context.soup.title else 'No Title'
        body = context.soup.find_all('p')
        text = ''.join(p.get_text() for p in body).strip()

        if origin_url not in data:
            data[origin_url] = []
        data[origin_url].append({
            'title': title,
            'text': text,
            'url': url
        })

        # Enqueue additional links and track the link that it came from
        await context.enqueue_links(
            label = origin_url
        )

    i =0
    batch_size = 1
    for i in range(0,len(urls),batch_size):
        url = urls[i:i+batch_size]
        await crawler.run(url)
        i+=batch_size

    # Write data to JSON files grouped by origin_seed
    output_dir = 'undergraduates_crawl'
    os.makedirs(output_dir, exist_ok=True)

    for origin_seed, origin_seed_data in data.items():
        filename = sanitize_filename(origin_seed) + '.json'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(origin_seed_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    asyncio.run(main())
