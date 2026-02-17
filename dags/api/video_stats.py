import os
from typing import Any, Dict, Final, Generator

import requests
from dotenv import load_dotenv

# Find the .env file somewhere from this file on up to root.
load_dotenv()
API_KEY_ENV: Final[str | None] = os.getenv("API_KEY")
API_KEY: Final[str] = API_KEY_ENV if API_KEY_ENV is not None else ""
CHANNEL_HANDLE: Final[str] = "MrBeast"
MAX_BATCH: Final[int] = 50


def get_playlist_id(channel_handle: str, api_key: str) -> str:
    try:
        url: Final[str] = (
            f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"
        )

        response: requests.Response = requests.get(url=url)

        json_response: Any = response.json()

        channel_item = json_response["items"][0]

        channel_playlistId = channel_item["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]

        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e


def get_video_ids(
    play_list_id: str, api_key: str, max_results: int = MAX_BATCH
) -> list[str]:
    try:
        video_ids: list[str] = []
        page_token = None  # needed for looping through pages

        base_url: Final[str] = (
            f"https://youtube.googleapis.com/youtube/v3/playlistItems?key={api_key}&playlistId={play_list_id}&maxResults={max_results}&part=contentDetails"
        )

        while True:
            curr_url = (
                base_url + f"&pageToken={page_token}"
                if page_token is not None
                else base_url
            )

            response: requests.Response = requests.get(url=curr_url)

            response.raise_for_status()

            json_response: Any = response.json()
            for item in json_response.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])

            page_token = json_response.get("nextPageToken")
            if page_token is None:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


def batch_list(
    video_ids: list[str], batch_size: int = MAX_BATCH
) -> Generator[list[str], Any, Any]:
    for batch_index in range(0, len(video_ids), batch_size):
        yield video_ids[batch_index : batch_index + batch_size]


def extract_video_data(
    video_ids: list[str], api_key: str, batch_size: int = MAX_BATCH
) -> list[Dict[str, Any]]:
    try:
        video_data_extracts = []

        for batch in batch_list(video_ids=video_ids, batch_size=batch_size):
            batch_ids = ",".join(batch)
            url: str = (
                f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={batch_ids}&key={api_key}&"
            )

            response: requests.Response = requests.get(url=url)
            json_response: Any = response.json()

            for item in json_response.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None),
                }
                video_data_extracts.append(video_data)

        return video_data_extracts
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    list_id = get_playlist_id(channel_handle=CHANNEL_HANDLE, api_key=API_KEY)
    video_ids = get_video_ids(play_list_id=list_id, api_key=API_KEY)
    video_data_extracts = extract_video_data(video_ids, API_KEY)

    print(f"{video_data_extracts}")
else:
    print(f"Current invocation is from {__name__}")
