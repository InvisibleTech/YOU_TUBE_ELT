# You Tube ETL

## Goal

To get some guided hands on, at speed, using a REST API to pull data into a Warehouse. In addition, will work with Airflow here which allows some understanding when I port this to [Dagster](https://dagster.io/) because [Dagster](https://dagster.io/) provides a comparison.

Wish me luck.

## What Are We Pulling In?

```json
{
  "kind": "youtube#videoListResponse",
  "etag": "fvAy6Z-9EDUJ_NeFuxrttzknRvo",
  "items": [
    {
      "kind": "youtube#video",
      "etag": "0Hw6bwu0Z2-9oD6ZFWc1QSPqjBs",
      "id": "8bMh8azh3CY",
      "statistics": {
        "viewCount": "128519601",
        "likeCount": "1820974",
        "favoriteCount": "0",
        "commentCount": "71334"
      }
    }
  ],
  "pageInfo": {
    "totalResults": 1,
    "resultsPerPage": 1
  }
}
```

specifically the `statistics` section. We are using the API

```bash
https://www.googleapis.com/youtube/v3/videos?id=[ID]&part=statistics&key=[API Key]
```

The security of this is okay against casual intrusion and it would require more effort to get the key parameter - the most likely leaking would be on the server side logs. Since we are not using this API from several IP addresses, the only restriction we have on the API is to be against Youtube only and for public data. We just don't feel like doing more for this tutorial and will retire the key when done.

We also need to get data from other APIs. Like for example, we need to get those video IDs.

- Channels to get the Playlist IDs
- Playlist Items to get the Video IDs
- Video Data to get the stats

## Appendix

## Pyenv

I felt like using `pyenv` since I had adopted it long ago. So I also use `pyenv virtualenv` - but I don't force my "religion" on you. Use whatever you want, I followed the tutorial and made sure this would work for good old `venv` and not commit monster cruft to your repo.

### Udemy Tutorial

This code is derived from working along with the training provided by the course [Data Engineering Project SQL, Python, Airflow, Docker, CI/CD
](https://www.udemy.com/course/start-your-data-engineering-journey-project-based-learning/).
