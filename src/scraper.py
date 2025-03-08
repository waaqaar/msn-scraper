"""
Module for scraping MSN News Feed.

This script retrieves MSN News Feed credentials, intercepts network requests 
using Playwright, and fetches the most liked article from the news feed.
"""

import os
import time
import json
import asyncio
import argparse

import requests
from fake_useragent import UserAgent
from playwright.async_api import async_playwright

# Path to store MSN News Feed credentials
MSN_NEWS_FEED_CREDENTIALS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "msn_news_feed.json"
)


def get_msn_news_feed_credentials():
    """
    Retrieve MSN News Feed credentials from the stored file.

    Returns:
        dict or None: Credentials if available, otherwise None.
    """
    if os.path.exists(MSN_NEWS_FEED_CREDENTIALS_FILE):
        with open(MSN_NEWS_FEED_CREDENTIALS_FILE, "r") as fp:
            return json.load(fp)


async def retrieve_msn_news_feed_credentials():
    """
    Retrieve and store MSN News Feed credentials by intercepting network requests.
    """
    async with async_playwright() as p:
        async def handle_route(route):
            request = route.request
            if "service/news/feed/pages/channelfeed" in request.url:
                with open(MSN_NEWS_FEED_CREDENTIALS_FILE, "w") as fp:
                    json.dump(
                        {
                            "url": request.url,
                            "method": request.method,
                            "headers": request.headers,
                        },
                        fp,
                        indent=4,
                    )
            await route.continue_()

        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--remote-debugging-port=9222"],
        )

        ua = UserAgent()
        context = await browser.new_context(
            user_agent=ua.random,
            extra_http_headers={
                "sec-ch-ua": '"Google Chrome";v="110", "Not-A.Brand";v="99", "Chromium";v="110"',
            },
        )

        page = await context.new_page()
        await page.route("**/*", handle_route)
        await page.goto("https://www.msn.com/en-us/channel/topic/Science/tp-Y_3304d105-5132-427d-b027-2f472f2fac07")

        time.sleep(5)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        await browser.close()


def retrieve_msn_news_feed_credentials_if_required():
    """
    Ensure MSN News Feed credentials are available; retrieve them if necessary.

    Returns:
        dict: The retrieved credentials.
    """
    credentials = get_msn_news_feed_credentials()
    if credentials:
        return credentials

    asyncio.run(retrieve_msn_news_feed_credentials())
    return get_msn_news_feed_credentials()


def get_msn_news_feed_article_with_most_likes(max_scans: int = 100, only_type: str = "all"):
    """
    Fetch the MSN News Feed article with the highest number of likes.

    Args:
        max_scans (int): Maximum number of results to scan.
        only_type (str): Filter by type (e.g., "all", "article", "video", "webcontent").

    Returns:
        tuple: (Most liked article as dict, Total likes as int).
    """
    credentials = retrieve_msn_news_feed_credentials_if_required()
    url = credentials["url"]

    scans = 0
    result_with_most_likes = None
    most_likes = -1

    while scans < max_scans:
        response = requests.get(url, headers=credentials["headers"])
        try:
            response.raise_for_status()
            response = response.json()
            url = response["nextPageUrl"]
            results = response["sections"][0]["cards"]

            for result in results:
                if only_type != "all" and result["type"] != only_type:
                    continue

                for reaction in result["reactionSummary"].get("subReactionSummaries", []):
                    if reaction["type"] == "upvote" and reaction["totalCount"] > most_likes:
                        most_likes = reaction["totalCount"]
                        result_with_most_likes = {
                            "id": result["id"],
                            "type": result["type"],
                            "category": result["category"],
                            "title": result["title"],
                            "abstract": result["abstract"],
                            "url": result["url"],
                            "provider": result["provider"],
                        }

            scans += len(results)
            print(
                "Scanning progress:",
                min(round((scans / max_scans) * 100, 2), 100.0),
                "%",
                (
                    f" [ Most likes so far: {most_likes}, URL: {result_with_most_likes['url']} ]"
                    if result_with_most_likes
                    else ""
                ),
            )
        except requests.exceptions.HTTPError:
            print("Failed to retrieve data. Retrying...")
            asyncio.run(retrieve_msn_news_feed_credentials())
            credentials = get_msn_news_feed_credentials()
            url = credentials["url"]
        except requests.exceptions.JSONDecodeError:
            if response.content == b"":
                print("No more results to scan.\nScanning progress: 100.0%")
                break
            else:
                raise

    return result_with_most_likes, most_likes


def main():
    """
    Parse command-line arguments and find the most liked MSN News Feed result.
    """
    parser = argparse.ArgumentParser(description="Scrape MSN News Feed for the result with most likes.")

    parser.add_argument("--max-scans", type=int, default=120, help="Maximum number of results to scan.")
    parser.add_argument("--only-type", type=str, default="all", help="Filter results by type: all, article, video, webcontent, etc.")

    args = parser.parse_args()

    result, total_likes = get_msn_news_feed_article_with_most_likes(max_scans=args.max_scans, only_type=args.only_type)

    print(
        f"\n\nThe 'type={args.only_type}' result with most likes in top {args.max_scans} results is:\n",
        json.dumps(result, indent=4),
    )
    print("\nTotal likes:\n", total_likes)


if __name__ == "__main__":
    main()
