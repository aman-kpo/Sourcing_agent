import os
from dotenv import load_dotenv

def test_env_vars():
    # Load environment variables
    load_dotenv()
    
    # Test each required API key
    required_keys = [
        'GOOGLE_API_KEY',
        'GOOGLE_SEARCH_ENGINE_ID',
        'OPENAI_API_KEY',
        'TAVILY_API_KEY'
    ]
    
    print("Testing environment variables...")
    all_present = True
    
    for key in required_keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key} is set")
        else:
            print(f"❌ {key} is not set")
            all_present = False
    
    if all_present:
        print("\nAll required environment variables are set!")
    else:
        print("\nSome environment variables are missing. Please check your .env file.")

if __name__ == "__main__":
    test_env_vars()
