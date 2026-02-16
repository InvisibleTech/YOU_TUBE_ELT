import os
from typing import Any, Final

import requests
from dotenv import load_dotenv

# Find the .env file somewhere from this file on up to root.
load_dotenv()
API_KEY: Final[str | None] = os.getenv("API_KEY")
CHANNEL_HANDLE: Final[str] = "MrBeast"


def get_playlist_id(channel_handle: str, api_key: str) -> str:
    try:
        url: Final[str] = (
            f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"
        )

        respone: requests.Response = requests.get(url=url)

        json_response: Any = respone.json()

        channel_item = json_response["items"][0]

        channel_playlistId = channel_item["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]

        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    list_id = get_playlist_id(channel_handle=CHANNEL_HANDLE, api_key=API_KEY)
    print(f"List id {list_id}")
else:
    print(f"Current invocation is from {__name__}")
