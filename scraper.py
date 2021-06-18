
from requests_html import HTML
from aiohttp import ClientSession
import asyncio

url = 'https://coreyms.com/'



async def fetch(url,session):
    '''Fetching the html page'''

    html_body = ""
    async with session.get(url) as response:
        response.raise_for_status
        html_body = await response.read()

        return html_body

async def main():
    '''Scraping the corey's website'''
    
    async with ClientSession() as session:
        
        task = asyncio.create_task(
            fetch(url,session)
        )
        page_content = await asyncio.gather(task)
        
        # writing the html in local
        
        with open('Outputs/index.html','w') as f:
            f.write(page_content[0].decode())
        
        



if __name__ == '__main__':

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    print('Code Completed 🔥')