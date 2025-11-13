#!/usr/bin/env python
"""
Test all pages of the Bionic Hand System
"""
import requests
import sys

def test_pages():
    """Test all pages"""
    print("=" * 60)
    print("🧪 Testing Bionic Hand System Pages")
    print("=" * 60)
    print()
    
    base_url = "http://127.0.0.1:8000"
    
    pages = [
        ('Home', '/'),
        ('About', '/about/'),
        ('Components', '/components/'),
        ('Circuit', '/circuit/'),
        ('Simulation', '/simulation/'),
        ('Research', '/research/'),
        ('Progress', '/progress/'),
        ('Contact', '/contact/'),
    ]
    
    passed = 0
    failed = 0
    
    for name, path in pages:
        url = base_url + path
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name:15} → {url:40} [OK]")
                passed += 1
            else:
                print(f"❌ {name:15} → {url:40} [Status: {response.status_code}]")
                failed += 1
        except Exception as e:
            print(f"❌ {name:15} → {url:40} [Error: {str(e)[:30]}]")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 All pages working perfectly!")
        return 0
    else:
        print(f"⚠️  {failed} page(s) failed")
        return 1

if __name__ == '__main__':
    try:
        exit_code = test_pages()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test error: {e}")
        sys.exit(1)
