import httpx

_client = httpx.AsyncClient(  # 设置全局客户端,是文档推荐的做法
    timeout=httpx.Timeout(30.0),
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    },
    follow_redirects=True,
)


async def fetch(url: str) -> str:
    """异步获取网页HTML内容"""
    resp = await _client.get(url)
    resp.raise_for_status()
    return resp.text
