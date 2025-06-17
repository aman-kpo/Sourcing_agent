import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_google_search():
    """Test Google Custom Search API directly"""
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    print(f"API Key: {api_key[:10]}..." if api_key else "No API key")
    print(f"Search Engine ID: {search_engine_id}")
    
    # Simple test query
    test_query = 'site:linkedin.com/in "software engineer" React'
    
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": test_query,
        "num": 5
    }
    
    print(f"\nTesting query: {test_query}")
    print(f"Request URL: https://www.googleapis.com/customsearch/v1")
    print(f"Params: {params}")
    
    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Total results: {results.get('searchInformation', {}).get('totalResults', 0)}")
            
            items = results.get("items", [])
            print(f"Items returned: {len(items)}")
            
            for i, item in enumerate(items):
                print(f"\n{i+1}. {item.get('title', 'No title')}")
                print(f"   URL: {item.get('link', 'No URL')}")
                print(f"   Snippet: {item.get('snippet', 'No snippet')[:100]}...")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_google_search() 