import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_grade_calculator():
    """Test the grade calculator endpoint"""
    try:
        data = {
            "best_grade": "10",
            "min_passing_grade": "4", 
            "your_grade": "8"
        }
        response = requests.post(f'{BASE_URL}/grade-calculator/calculate', json=data)
        print(f"Grade Calculator: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Grade Calculator Failed: {e}")
        return False

def test_cost_calculator():
    """Test the cost calculator endpoint"""
    try:
        data = {
            "selected_buckets": ["Bucket-1", "Bucket-2"]
        }
        response = requests.post(f'{BASE_URL}/cost-calculator/calculate', json=data)
        print(f"Cost Calculator: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Cost Calculator Failed: {e}")
        return False

def test_user_details():
    """Test storing user details"""
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890"
        }
        response = requests.post(f'{BASE_URL}/grade-calculator/user-details', json=data)
        print(f"User Details: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"User Details Failed: {e}")
        return False

def main():
    print("Testing Unified Study Calculator Backend...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Grade Calculator", test_grade_calculator),
        ("Cost Calculator", test_cost_calculator),
        ("User Details", test_user_details)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the backend configuration.")

if __name__ == "__main__":
    main()