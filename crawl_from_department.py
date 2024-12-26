import asyncio
import json
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
import os
from crawlee import ConcurrencySettings
import re
from collections import defaultdict  # Add this import

async def main() -> None:
    concurrency_settings = ConcurrencySettings(
        max_concurrency=20,
    )

    def sanitize_filename(filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    crawler = BeautifulSoupCrawler(max_crawl_depth=2, max_requests_per_crawl=20, concurrency_settings=concurrency_settings)
    # Use defaultdict to avoid needing to check if key exists
    data = defaultdict(list)

    def save_mapping(origin_seed, filename):
        try:
            with open('mapping_undergraduates.json', 'r', encoding='utf-8-sig') as f:
                mapping = json.load(f)
        except FileNotFoundError:
            mapping = {}
        mapping[origin_seed] = filename
        with open('mapping_undergraduates.json', 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=4)

    # Add error handling for seed URLs loading
    try:
        with open('undergraduates/undergraduates2.json', 'r', encoding='utf-8-sig') as f:
            degrees_json = json.load(f)
            urls = [item['department_url'] for item in degrees_json]
    except FileNotFoundError:
        print("Seeds file not found")
        return
    except json.JSONDecodeError:
        print("Invalid JSON in seeds file")
        return

    @crawler.router.default_handler
    async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
        try:
            url = context.request.url
            origin_url = url if url in urls else context.request.label
            
            title = context.soup.title.string.strip() if context.soup.title else 'No Title'
            body = context.soup.find_all('p')
            text = ''.join(p.get_text() for p in body).strip()

            # Using defaultdict, we can append directly without checking
            data[origin_url].append({
                'title': title,
                'text': text,
                'url': url
            })

            await context.enqueue_links(label=origin_url)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    batch_size = 1
    urls = urls
    for batch in [urls[i:i+batch_size] for i in range(0, len(urls), batch_size)]:
        await crawler.run(batch)

    # Save collected data
    output_dir = 'undergraduates_crawl'
    os.makedirs(output_dir, exist_ok=True)

    for origin_seed, origin_seed_data in data.items():   
        try:
            filename = sanitize_filename(origin_seed) + '.json'
            save_mapping(origin_seed, filename)
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(origin_seed_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data for {origin_seed}: {e}")

if __name__ == '__main__':
    asyncio.run(main())