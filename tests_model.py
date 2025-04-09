# test_model.py
import requests
import json

# API configuration
BASE_URL = "http://127.0.0.1:8000"

def login():
    """Get authentication token"""
    login_data =json.dumps( {
        "userName": "admin1@gmail.com",
        "password": "admin1111"
    })
    headers = {
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/docteur/api/login/"
    response = requests.request("POST", url, headers=headers, data=login_data)
    json_data = response.json()
    print('user connected:::',json_data['tokens']['access_token'])
    return json_data['tokens']['access_token']
  # Convertir en dictionnaire



def make_prediction(features, token):
    """Make prediction with given features"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/docteur/api/predict/",
        headers=headers,
        json={"features": features}
    )
    return response.json()

# Test cases - these are example values for the 10 most important features
test_cases = [
    # Test Case 1 - Malignant
    {
        "worst area": 1001.0,
        "worst concave points": 0.1602,
        "mean concave points": 0.07017,
        "worst radius": 25.38,
        "mean concavity": 0.0869,
        "worst perimeter": 184.6,
        "mean perimeter": 132.9,
        "mean radius": 20.57,
        "mean area": 1326.0,
        "worst concavity": 0.2505
    },
    # Test Case 2 - Benign
    {
        "worst area": 445.0,
        "worst concave points": 0.0398,
        "mean concave points": 0.02513,
        "worst radius": 14.34,
        "mean concavity": 0.06495,
        "worst perimeter": 96.2,
        "mean perimeter": 78.04,
        "mean radius": 12.05,
        "mean area": 449.3,
        "worst concavity": 0.2102
    },
    # Test Case 3 - Borderline
    {
        "worst area": 700.0,
        "worst concave points": 0.0804,
        "mean concave points": 0.04768,
        "worst radius": 18.22,
        "mean concavity": 0.07741,
        "worst perimeter": 121.4,
        "mean perimeter": 97.65,
        "mean radius": 15.13,
        "mean area": 711.8,
        "worst concavity": 0.1804
    },
    # Test Case 4 - Strong Malignant Indicators
    {
        "worst area": 1300.0,
        "worst concave points": 0.1508,
        "mean concave points": 0.12790,
        "worst radius": 28.11,
        "mean concavity": 0.1974,
        "worst perimeter": 198.8,
        "mean perimeter": 130.0,
        "mean radius": 19.69,
        "mean area": 1203.0,
        "worst concavity": 0.3005
    },
    # Test Case 5 - Strong Benign Indicators
    {
        "worst area": 387.0,
        "worst concave points": 0.0248,
        "mean concave points": 0.02037,
        "worst radius": 11.75,
        "mean concavity": 0.03285,
        "worst perimeter": 75.2,
        "mean perimeter": 73.17,
        "mean radius": 11.42,
        "mean area": 402.7,
        "worst concavity": 0.1003
    }
]


def run_tests():
    try:
        # Get authentication token
        token = login()
        print("Successfully logged in\n")

        # Run each test case
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print("Input features:")
            for feature, value in test_case.items():
                print(f"{feature}: {value}")
            
            # Convert dictionary to list maintaining feature order
            features_list = test_case
            
            # Make prediction
            result = make_prediction(features_list, token)
            
            print("\nPrediction Results:", result)
            print(f"Diagnosis: {result['prediction']}")
            print(f"Confidence: {result.get('confidence', 'N/A')}%")
            print(f"Severity: {result.get('severity', 'N/A')}")
            print(f"Message: {result.get('message', 'N/A')}")
            if 'recommended_actions' in result:
                print("\nRecommended Actions:")
                for action in result['recommended_actions']:
                    print(f"- {action}")
            print("\n" + "="*50)

    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    run_tests()