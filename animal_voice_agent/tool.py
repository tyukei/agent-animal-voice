from urllib.parse import quote

def search_animal_youtube(animal_name: str) -> str:
    """指定された動物の鳴き声に関するYouTube動画を検索します。
    
    Args:
        animal_name: 動物の名前（例: 犬、猫、ライオン）
        
    Returns:
        YouTube検索結果のURL
    """
    # 動物の鳴き声を検索するためのクエリを作成
    search_query = f"{animal_name} 鳴き声"
    encoded_query = quote(search_query)
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    return f"【{animal_name}の鳴き声】YouTube検索結果: {youtube_search_url}"


def get_animal_location_map(animal_name: str, location_name: str) -> str:
    """那覇空港から指定された場所までのGoogle Mapsルートリンクを生成します。
    
    Args:
        animal_name: 動物の名前（例: イリオモテヤマネコ、ヤンバルクイナ、ジンベエザメ）
        location_name: 目的地の名前（例: 美ら海水族館、ヤンバルクイナ生態展示学習施設）
        
    Returns:
        Google Mapsのルートリンク
    """
    # 那覇空港からのルートを生成
    origin = "那覇空港"
    destination = location_name
    
    # Google Maps URLを生成
    encoded_origin = quote(origin)
    encoded_destination = quote(destination)
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_destination}&travelmode=driving"
    
    return f"【{animal_name}が見られる場所へのルート】\n那覇空港 → {location_name}\n {maps_url}"