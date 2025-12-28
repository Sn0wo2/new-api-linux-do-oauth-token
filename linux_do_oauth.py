from typing import Optional

from curl_cffi import requests, Response
from linux_do_connect import LinuxDoConnect, IMPERSONATE

SESSION_KEY = "session"


class LinuxDoOAuth:
    def __init__(self, base_url: str, session: Optional[requests.AsyncSession] = requests.AsyncSession(),
                 client_id: str = ""):
        self.base_url = base_url
        self.session = session
        self.client_id = client_id

    async def fetch_client_id(self) -> "LinuxDoOAuth":
        r: Response = await self.session.get(f"{self.base_url}/api/status")

        json_data = r.json()

        if json_data.get("success") and "data" in json_data:
            self.client_id = json_data["data"].get("linuxdo_client_id", "")

        return self

    async def get_session(self) -> requests.AsyncSession:
        return self.session

    async def login(self, connect_token: str = "") -> Response:
        client = LinuxDoConnect()
        if connect_token:
            client.set_connect_token(connect_token)
        else:
            raise ValueError("No connect token provided")

        r: Response = await self.session.get(f"{self.base_url}/api/oauth/state")

        json_data = r.json()

        state = None
        if json_data.get("success") and "data" in json_data:
            state = json_data["data"]

        if not self.client_id or not state:
            raise ValueError("client_id or state not provided")

        callback_url = await client.approve_oauth(
            f"https://connect.linux.do/oauth2/authorize?response_type=code&client_id={self.client_id}&state={state}")

        return await self.session.get(callback_url.replace("/oauth/", "/api/oauth/", 1), impersonate=IMPERSONATE)
