import requests
import csv
import json
import asyncio
import tqdm
import aiohttp
import aiofiles
url = 'https://www.qimao.com/api/book/chapter-list?book_id=1809361'
pr=requests.get(url)
pr=pr.json()
pr_s=pr['data']['chapters']
for pr_ in tqdm.tqdm(pr_s):
    pr_id=pr_['id']
    pr_title=pr_['title']
#    print(pr_id)

async def xs(id,session):
        async with session.get(f'https://www.qimao.com/shuku/1809361-{id}/') as f:
            xs_j=await f.text()

            return xs_j
async def session(id):
    async with aiohttp.ClientSession() as session:
        content= await xs(id,session)
        return content
async def main():
    tasks=[]
    for pr_ in tqdm.tqdm(pr_s):
        pr_id=pr_['id']
        task=asyncio.create_task(session(pr_id))
        tasks.append(task)
        await asyncio.wait(tasks)
        async with aiofiles.open('text.csv','w',encoding='utf-8') as f:
            for tas in tasks:
                content=await task
                await f.write(content+'\n')
if __name__=='__main__':
    asyncio.run(main())







