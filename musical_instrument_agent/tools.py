import re
import requests
from urllib.parse import quote


def search_instrument_youtube(instrument_name: str) -> str:
    """指定された楽器の演奏に関するYouTube動画を検索します。上位1件の動画URLを返します。

    Args:
        instrument_name: 楽器の名前（例: ピアノ、ギター、バイオリン）

    Returns:
        YouTube検索結果のURL
    """
    # 楽器の演奏を検索するためのクエリを作成
    search_query = f"{instrument_name} 演奏"
    encoded_query = quote(search_query)
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    try:
        response = requests.get(youtube_search_url, timeout=10)
        if response.status_code != 200:
            return youtube_search_url
        html = response.text
    except requests.exceptions.RequestException:
        return youtube_search_url

    # 検索結果ページ内の watch?v=VIDEO_ID を雑に1個拾う（壊れやすい）
    m = re.search(r"watch\?v=([a-zA-Z0-9_-]{11})", html)
    if not m:
        return youtube_search_url  # 取れなければ検索結果URLを返すなど

    vid = m.group(1)
    return f"https://www.youtube.com/watch?v={vid}"


def get_instrument_shop_map(shop_name: str) -> str:
    """渋谷駅から指定された楽器店までのGoogle Mapsルートリンクを生成します。

    Args:
        shop_name: 楽器店の名前（例: イケベ楽器、島村楽器）

    Returns:
        Google Mapsのルートリンク
    """
    # 渋谷駅からのルートを生成
    origin = "渋谷駅"
    destination = shop_name

    # Google Maps URLを生成
    encoded_origin = quote(origin)
    encoded_destination = quote(destination)
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_destination}&travelmode=driving"

    return maps_url
