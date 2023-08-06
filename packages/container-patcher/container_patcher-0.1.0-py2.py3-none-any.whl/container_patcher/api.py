import urllib.request
import urllib.error
import json
import asyncio


async def get_search_repo(query):
    params = {'q': query}
    url = 'https://api.github.com/search/repositories'
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, urllib.request.urlopen, req)
    return json.load(res)['items'][0]


async def get_search_commits(repo_name, query):
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    url = f'https://api.github.com/search/commits?q=repo:{repo_name}+{query}'
    req = urllib.request.Request(url, headers=headers)
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, urllib.request.urlopen, req)
    return json.load(res)['items']


async def get_search_issues(repo_name, query):
    url = f'https://api.github.com/search/issues?q=repo:{repo_name}+{query}'
    req = urllib.request.Request(url)
    loop = asyncio.get_event_loop()
    res = await  loop.run_in_executor(None, urllib.request.urlopen, req)
    return json.load(res)['items']


async def get_pull_commits(repo_name, pull_num):
    url = f'htpps://api.github.com/repos/{repo_name}/pulls/{pull_num}/commits'
    req = urllib.request.Request(url)
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, urllib.request.urlopen, req)
    return json.load(res)
