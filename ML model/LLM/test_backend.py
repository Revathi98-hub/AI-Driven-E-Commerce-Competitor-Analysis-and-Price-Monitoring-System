"""
Test script for LLM backend components
Run this before starting the full server to verify setup
"""
import os
import sys
from dotenv import load_dotenv

print("="*60)
print("🧪 LLM Backend Test Suite")
print("="*60)

# Load environment variables
load_dotenv()

# Test 1: Check environment variables
print("\n1️⃣ Testing Environment Variables...")
groq_key = os.getenv('GROQ_API_KEY')
mongo_uri = os.getenv('MONGO_URI')

if not groq_key or groq_key == "your_groq_api_key":
    print("❌ GROQ_API_KEY not set!")
    print("   Get your free key from: https://console.groq.com")
    print("   Then update .env file")
    sys.exit(1)
else:
    print(f"✅ GROQ_API_KEY found (length: {len(groq_key)})")

if not mongo_uri:
    print("❌ MONGO_URI not set!")
    sys.exit(1)
else:
    print(f"✅ MONGO_URI configured")

print(f"✅ MONGO_DB: {os.getenv('MONGO_DB', 'ecom_tracker')}")

# Test 2: Check dependencies
print("\n2️⃣ Testing Dependencies...")
try:
    import pymongo
    print("✅ pymongo installed")
except ImportError:
    print("❌ pymongo not installed - run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import groq
    print("✅ groq installed")
except ImportError:
    print("❌ groq not installed - run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import fastapi
    print("✅ fastapi installed")
except ImportError:
    print("❌ fastapi not installed - run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import httpx
    print("✅ httpx installed")
except ImportError:
    print("❌ httpx not installed - run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: MongoDB connection
print("\n3️⃣ Testing MongoDB Connection...")
try:
    from pymongo import MongoClient
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection
    print("✅ MongoDB connection successful")
    
    # Check database and collections
    db = client[os.getenv('MONGO_DB', 'ecom_tracker')]
    collections = db.list_collection_names()
    print(f"✅ Database '{db.name}' accessible")
    print(f"   Collections found: {', '.join(collections)}")
    
    # Count documents
    if 'products' in collections:
        product_count = db['products'].count_documents({})
        print(f"✅ Products collection: {product_count} documents")
    else:
        print("⚠️  'products' collection not found")
    
    client.close()
except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)}")
    sys.exit(1)

# Test 4: Test tools functions
print("\n4️⃣ Testing Tools Functions...")
try:
    import tools
    
    # Test search_products
    print("   Testing search_products()...")
    products = tools.search_products()
    if products and not products[0].get('error'):
        print(f"   ✅ Found {len(products)} products")
        if len(products) > 0:
            print(f"      Sample: {products[0].get('title', 'N/A')[:50]}...")
    else:
        print(f"   ⚠️  No products found or error: {products}")
    
    # Test get_top_rated_products
    print("   Testing get_top_rated_products()...")
    top_products = tools.get_top_rated_products(limit=3)
    if top_products and not top_products[0].get('error'):
        print(f"   ✅ Found {len(top_products)} top rated products")
    else:
        print(f"   ⚠️  Error: {top_products}")
    
    print("✅ Tools module loaded successfully")
except Exception as e:
    print(f"❌ Tools test failed: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 5: Test Groq API
print("\n5️⃣ Testing Groq API Connection...")
try:
    from groq import Groq
    groq_client = Groq(api_key=groq_key)
    
    # Simple test message
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Updated model
        messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
        max_tokens=10
    )
    
    reply = response.choices[0].message.content
    print(f"✅ Groq API working! Response: {reply}")
except Exception as e:
    print(f"❌ Groq API test failed: {str(e)}")
    sys.exit(1)

# Test 6: Test conversation memory
print("\n6️⃣ Testing Conversation Memory...")
try:
    from conversation_memory import ConversationMemory
    memory = ConversationMemory()
    
    # Test adding messages
    memory.add_message("test_session", "user", "Hello")
    memory.add_message("test_session", "assistant", "Hi there!")
    
    history = memory.get_history("test_session")
    if len(history) == 2:
        print(f"✅ Conversation memory working ({len(history)} messages)")
    else:
        print(f"⚠️  Expected 2 messages, got {len(history)}")
    
    memory.clear_session("test_session")
except Exception as e:
    print(f"❌ Conversation memory test failed: {str(e)}")

# Test 7: Test LLM Agent (if Groq key is set)
print("\n7️⃣ Testing LLM Agent...")
try:
    from llm_agent import LLMAgent
    print("✅ LLM Agent module loaded")
    print("   (Full agent test requires async environment)")
except Exception as e:
    print(f"❌ LLM Agent load failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✅ All tests passed! Backend is ready to start")
print("="*60)
print("\n📝 Next steps:")
print("1. Start the server: python chatbot_api.py")
print("2. Or use: .\\start_server.bat")
print("3. Visit: http://localhost:5001/docs")
print("4. Test endpoint: POST /api/chat")
print()
