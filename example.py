import asyncio
import os

from linux_do_oauth import LinuxDoOAuth, SESSION_KEY


async def main():
    oauth = LinuxDoOAuth(base_url="https://x666.me")
    r = await (await oauth.fetch_client_id()).login(connect_token=os.getenv("LINUX_DO_CONNECT_TOKEN"))

    print("status:", r.status_code)
    print(r.text)
    print((await oauth.get_session()).cookies.get(SESSION_KEY, domain="x666.me"))


if __name__ == '__main__':
    asyncio.run(main())
