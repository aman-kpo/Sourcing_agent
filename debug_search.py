import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

def debug_specific_query():
    """Debug the specific query that returned 0 results"""
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    # The query that failed
    failed_query = 'site:linkedin.com/in "DevOps Engineer" "Information Technology" "Startup" "San Francisco, California"'
    
    print(f"Testing failed query: {failed_query}")
    
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": failed_query,
        "num": 10
    }
    
    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Total results: {results.get('searchInformation', {}).get('totalResults', 0)}")
            
            items = results.get("items", [])
            print(f"Items returned: {len(items)}")
            
            if len(items) == 0:
                print("\n❌ No items found. Let's try simpler queries...")
                
                # Test simpler queries
                simple_queries = [
                    'site:linkedin.com/in "DevOps Engineer"',
                    'site:linkedin.com/in DevOps Engineer',
                    'site:linkedin.com/in "Software Engineer" San Francisco',
                    'site:linkedin.com/in Engineer'
                ]
                
                for i, simple_query in enumerate(simple_queries):
                    print(f"\n--- Testing simple query {i+1}: {simple_query} ---")
                    simple_params = {
                        "key": api_key,
                        "cx": search_engine_id,
                        "q": simple_query,
                        "num": 3
                    }
                    
                    simple_response = requests.get("https://www.googleapis.com/customsearch/v1", params=simple_params)
                    if simple_response.status_code == 200:
                        simple_results = simple_response.json()
                        simple_items = simple_results.get("items", [])
                        print(f"Found {len(simple_items)} results")
                        
                        if simple_items:
                            for j, item in enumerate(simple_items[:2]):
                                print(f"  {j+1}. {item.get('title', 'No title')}")
                                print(f"     URL: {item.get('link', 'No URL')}")
                    else:
                        print(f"Error: {simple_response.status_code}")
            else:
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
    debug_specific_query() 