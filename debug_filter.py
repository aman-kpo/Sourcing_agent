import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_url_filtering():
    """Check what LinkedIn URLs actually look like from the API"""
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    query = 'site:linkedin.com/in "DevOps Engineer" "Information Technology" "Startup" "San Francisco, California"'
    
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": 10
    }
    
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    results = response.json()
    
    print("=== ALL ITEMS FROM API ===")
    for i, item in enumerate(results.get("items", [])):
        url = item.get("link", "")
        title = item.get("title", "")
        print(f"\n{i+1}. Title: {title}")
        print(f"   URL: {url}")
        print(f"   Contains 'linkedin.com/in/': {'linkedin.com/in/' in url}")
        print(f"   Contains 'linkedin.com/in': {'linkedin.com/in' in url}")
        print(f"   Contains '/in/': {'/in/' in url}")
    
    print("\n" + "="*50)
    print("FILTERING TEST:")
    
    # Test current filter
    profiles_current = []
    for item in results.get("items", []):
        if "linkedin.com/in/" in item.get("link", ""):
            profiles_current.append(item)
    print(f"Current filter ('linkedin.com/in/'): {len(profiles_current)} profiles")
    
    # Test improved filter  
    profiles_improved = []
    for item in results.get("items", []):
        link = item.get("link", "")
        if "linkedin.com/in" in link and not link.endswith("/dir"):
            profiles_improved.append(item)
    print(f"Improved filter ('linkedin.com/in' + not dir): {len(profiles_improved)} profiles")
    
    # Show what we'd get with improved filter
    if profiles_improved:
        print("\nWith improved filter, we'd get:")
        for i, item in enumerate(profiles_improved[:3]):
            print(f"  {i+1}. {item.get('title', 'No title')}")
            print(f"     {item.get('link', 'No URL')}")

if __name__ == "__main__":
    debug_url_filtering() 