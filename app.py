import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_webpage(url, max_length=10000, start_index=0, raw=False):
    """
    Fetch web content via API and parse RSS if detected

    Args:
        url (str): URL to fetch
        max_length (int): Maximum length of returned content
        start_index (int): Starting index
        raw (bool): Whether to return raw content

    Returns:
        dict: API response or parsed RSS content
    """
    api_url = "http://0.0.0.0:8000/fetch"
    headers = {"Content-Type": "application/json"}

    payload = {
        "url": url,
        "max_length": max_length,
        "start_index": start_index,
        "raw": raw
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        # First try to get the response as text
        response_text = response.text

        # Check if the response is XML content directly
        if response_text.strip().startswith('<?xml') or response_text.strip().startswith('<rss'):
            return parse_rss_feed(response_text)

        # Try to parse as JSON if not XML
        try:
            response_data = response.json()
            # Check if it's a dictionary with a content field that contains XML
            if isinstance(response_data, dict) and 'content' in response_data:
                if isinstance(response_data['content'], str) and (
                    response_data['content'].strip().startswith('<?xml') or
                    response_data['content'].strip().startswith('<rss')
                ):
                    return parse_rss_feed(response_data['content'])
            return response_data
        except json.JSONDecodeError:
            # Not JSON, return the text content
            return {"content": response_text}

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"error": str(e)}

def parse_rss_feed(xml_content):
    """
    Parse RSS feed content

    Args:
        xml_content (str): RSS XML content

    Returns:
        dict: Parsed RSS content
    """
    try:
        root = ET.fromstring(xml_content)
        channel = root.find('channel')

        feed_data = {
            "title": channel.findtext('title', ''),
            "description": channel.findtext('description', ''),
            "link": channel.findtext('link', ''),
            "items": []
        }

        for item in channel.findall('item'):
            pub_date = item.findtext('pubDate', '')

            item_data = {
                "title": item.findtext('title', ''),
                "link": item.findtext('link', ''),
                "pubDate": pub_date,
                "description": item.findtext('description', ''),
                "categories": [cat.text for cat in item.findall('category')]
            }
            feed_data["items"].append(item_data)

        return {"rss_feed": feed_data}
    except Exception as e:
        return {"error": f"RSS parsing failed: {str(e)}"}

if __name__ == "__main__":
    # Example usage
    result = fetch_webpage(
        url="https://www.techradar.com/au/feeds/tag/computing",
        max_length=100000,  # Increase limit for RSS feeds
        start_index=0,
        raw=True
    )

    print(json.dumps(result, indent=2))