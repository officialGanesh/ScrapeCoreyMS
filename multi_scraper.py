
import csv
from requests.sessions import session
from requests_html import HTML
from aiohttp import ClientSession
import asyncio



async def fetch(url,session):
    '''Fetching the html page'''

    html_body = ""
    async with session.get(url) as response:
        response.raise_for_status
        html_body = await response.read()

        return html_body


async def main():
    """Scraping the corey's website"""
    
    async with ClientSession() as session:
        
        for i in range(2,18):
            url = f'https://coreyms.com/page/{i}'
            task = asyncio.create_task(
                fetch(url,session)
            )
            page_content = await asyncio.gather(task)
            
            # writing the html in local
            
            with open(f'Outputs/multi/page{i}.html','w') as f:
                f.write(page_content[0].decode())
            
            # Reading the html in local
            with open(f'Outputs/multi/page{i}.html','r') as f:
                source = f.read()
                html_str = HTML(html=source)
            
            

            # page check
            title_box = html_str.find('.title-area',first=True)
            print(title_box.text)

            # writing data in csv
            csv_file = open(f'Outputs\multi\csvFiles\page{i}.csv','w',newline='')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Title','Published','Author','Project_desc','Video'])

            posts = html_str.find('.post')

            
            for post in posts:
                headline = post.find('.entry-title',first=True).text
                # print(headline)

                date = post.find('.entry-time',first=True).text
                # print(date)

                author = post.find('.entry-author-name',first=True).text
                # print(author)

                content_box = post.find('.entry-content',first=True)
                project_desc = content_box.find('p',first=True).text
                # print(project_desc)

                # for youtube video links
                
                try:

                    vid_link = content_box.find('iframe',first=True).attrs['src'].split('?')[0]
                    yt_link = f"https://www.youtube.com/watch?v={vid_link.split('/')[4]}"
                    # print(yt_link)

                except Exception as e:
                    print(url, '😄')
                    # print('Something went wrong ',e)

                csv_writer.writerow([headline,date,author,project_desc,yt_link])
            csv_file.close()

        
if __name__ == '__main__':

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    print('Code Completed 🔥')