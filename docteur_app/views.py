import os
import json
import joblib
import numpy as np
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user
from rest_framework.response import Response
from django.views.generic.edit import View
from rest_framework import status
import logging
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate,login, logout
from django.middleware.csrf import get_token




class UserRegistrationView(APIView):
    permission_classes = []
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request, *args, **kwargs):
        print('çççççççççç')
        serializer = UserRegistrationSerializer(data=request.data)
        print(f'the serializer datas are :{serializer}')
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        print(f'Error:::{serializer.errors}')
        return render(request, 'register.html', {'error': 'Mot de passe incohérents ou email existe déjà'})


logger = logging.getLogger(__name__)

class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print(f'data:::{request.data}')
        username = request.data.get('userName')
        password = request.data.get('password')
        print(f'datas are :{username} and {password}')
        user = authenticate(request, username=username, password=password)
        print(f'user found is : {user}')
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successfull", "tokens": tokens}
            print(f'response:::{response}')
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})
    def get(self, request):
        content = {"user": str(request.user), 
                   "auth": str(request.auth)}
        
        return Response(data=content, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print(f'data:::{request.data}')
        username = request.data.get('userName')
        password = request.data.get('password')
        print(f'datas are :{username} and {password}')
        user = authenticate(request, username=username, password=password)
        print(f'user found is : {user}')
        if user:
            login(request, user)
            next_url = request.GET.get("redirect_to")
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
            # return render(request, 'dashboard.html')
        return render(request, 'login.html', {'error': 'Identifiants invalides'})

class LogoutView(View):
    def get(self, request):
        logger.info(f"user {self.request.user.email} disconnected")
        logout(request)
        return redirect("/docteur/login")

class DashboardView(LoginRequiredMixin, View):
    login_url = "/docteur/login/"
    redirect_field_name = "redirect_to"
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return render(request, 'dashboard.html')
    
    def post(self, request):
        if final_model is None or scaler_top is None:
            return render(request, 'dashboard.html', {"error": "Model not initialized"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            current_user = request.user
            if not current_user.is_active:
                return render(request, 'dashboard.html', {"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

            request_data = {
            "worst area": request.POST.get('worst_area'),
            "worst concave points": request.POST.get('worst_concave_points'),
            "mean concave points": request.POST.get('mean_concave_points'),
            "worst radius": request.POST.get('worst_radius'),
            "mean concavity": request.POST.get('mean_concavity'),
            "worst perimeter": request.POST.get('worst_perimeter'),
            "mean perimeter": request.POST.get('mean_perimeter'),
            "mean radius": request.POST.get('mean_radius'),
            "mean area": request.POST.get('mean_area'),
            "worst concavity": request.POST.get('worst_concavity')
            }
            data = {'features' : request_data}
            
            # Handle dictionary input format
            if not isinstance(data, dict) or 'features' not in data:
                return Response({
                    "error": "Invalid input format",
                    "message": "Expected format: {'features': {feature_name: value, ...}}",
                    "example": {
                        "features": {
                            "worst area": 515.8,
                            "worst concave points": 0.0737,
                            # ... other features
                        }
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            features_dict = data['features']
            
            # Validate all required features are present
            missing_features = set(REQUIRED_FEATURES) - set(features_dict.keys())
            if missing_features:
                return render(request, 'dashboard.html', {
                    "error": "Missing features",
                    "missing_features": list(missing_features),
                    "required_features": REQUIRED_FEATURES
                }, status=status.HTTP_400_BAD_REQUEST)

            # Convert dictionary to ordered list based on feature importance
            features_list = [features_dict[feature] for feature in REQUIRED_FEATURES]

            # Validate numerical values
            if not all(isinstance(x, (int, float)) for x in features_list):
                return render(request, 'dashboard.html',{
                    "error": "Invalid feature values",
                    "message": "All features must be numerical values"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Make prediction
            input_data = np.array(features_list).reshape(1, -1)
            scaled_data = scaler_top.transform(input_data)
            prediction = final_model.predict(scaled_data)
            probabilities = final_model.predict_proba(scaled_data)[0]
            
            result = "malignant" if prediction[0] == 0 else "benign"
            confidence = float(probabilities[0] if result == "malignant" else probabilities[1])

            response = {
                "prediction": result,
                "confidence": round(confidence * 100, 2),
                "features_received": {
                    feature: value for feature, value in zip(REQUIRED_FEATURES, features_list)
                }
            }

            if result == "malignant":
                response.update({
                    "severity": "High Risk",
                    "message": "Please consult a doctor immediately.",
                    "recommended_actions": [
                        "Schedule immediate follow-up",
                        "Prepare medical history",
                        "Contact oncology department"
                    ]
                })
            else:
                response.update({
                    "severity": "Low Risk",
                    "message": "No immediate action required.",
                    "recommended_actions": [
                        "Continue regular check-ups",
                        "Schedule next screening as recommended"
                    ]
                })

            return render(request, 'dashboard.html', {"data" : response}, status=status.HTTP_200_OK)

        except Exception as e:
            return render(request, 'dashboard.html',{
                "error": "Prediction failed",
                "message": str(e),
                "required_features": REQUIRED_FEATURES
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Load the model, scaler, and feature information
try:
    base_dir = settings.BASE_DIR
    model_path = os.path.join(base_dir, 'final_model.pkl')
    scaler_path = os.path.join(base_dir, 'scaler_top.pkl')
    feature_info_path = os.path.join(base_dir, 'feature_info.json')
    
    final_model = joblib.load(model_path)
    scaler_top = joblib.load(scaler_path)
    
    with open(feature_info_path, 'r') as f:
        feature_info = json.load(f)
    
    REQUIRED_FEATURES = feature_info['features']
    print("Model, scaler, and feature info loaded successfully")
    
except Exception as e:
    print(f"Error loading files: {str(e)}")
    final_model = None
    scaler_top = None
    feature_info = None
    REQUIRED_FEATURES = []
    
class PredictAPIView(APIView):
    permission_classes = [IsAuthenticated]
    login_url = "/docteur/login/"
    redirect_field_name = "redirect_to"

    def post(self, request):
        if final_model is None or scaler_top is None:
            return Response({"error": "Model not initialized"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            current_user = request.user
            if not current_user.is_active:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            
            # Handle dictionary input format
            if not isinstance(data, dict) or 'features' not in data:
                return Response({
                    "error": "Invalid input format",
                    "message": "Expected format: {'features': {feature_name: value, ...}}",
                    "example": {
                        "features": {
                            "worst area": 515.8,
                            "worst concave points": 0.0737,
                            # ... other features
                        }
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            features_dict = data['features']
            
            # Validate all required features are present
            missing_features = set(REQUIRED_FEATURES) - set(features_dict.keys())
            if missing_features:
                return Response({
                    "error": "Missing features",
                    "missing_features": list(missing_features),
                    "required_features": REQUIRED_FEATURES
                }, status=status.HTTP_400_BAD_REQUEST)

            # Convert dictionary to ordered list based on feature importance
            features_list = [features_dict[feature] for feature in REQUIRED_FEATURES]

            # Validate numerical values
            if not all(isinstance(x, (int, float)) for x in features_list):
                return Response({
                    "error": "Invalid feature values",
                    "message": "All features must be numerical values"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Make prediction
            input_data = np.array(features_list).reshape(1, -1)
            scaled_data = scaler_top.transform(input_data)
            prediction = final_model.predict(scaled_data)
            probabilities = final_model.predict_proba(scaled_data)[0]
            
            result = "malignant" if prediction[0] == 0 else "benign"
            confidence = float(probabilities[0] if result == "malignant" else probabilities[1])

            response = {
                "prediction": result,
                "confidence": round(confidence * 100, 2),
                "features_received": {
                    feature: value for feature, value in zip(REQUIRED_FEATURES, features_list)
                }
            }

            if result == "malignant":
                response.update({
                    "severity": "High Risk",
                    "message": "Please consult a doctor immediately.",
                    "recommended_actions": [
                        "Schedule immediate follow-up",
                        "Prepare medical history",
                        "Contact oncology department"
                    ]
                })
            else:
                response.update({
                    "severity": "Low Risk",
                    "message": "No immediate action required.",
                    "recommended_actions": [
                        "Continue regular check-ups",
                        "Schedule next screening as recommended"
                    ]
                })

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "Prediction failed",
                "message": str(e),
                "required_features": REQUIRED_FEATURES
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if final_model is None or scaler_top is None:
            return render(request, 'dashboard.html', {"error": "Model not initialized"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            current_user = request.user
            if not current_user.is_active:
                return render(request, 'dashboard.html', {"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

            request_data = {
            "worst area": request.data.get('worst_area'),
            "worst concave points": request.data.get('worst_concave_points'),
            "mean concave points": request.data.get('mean_concave_points'),
            "worst radius": request.data.get('worst_radius'),
            "mean concavity": request.data.get('mean_concavity'),
            "worst perimeter": request.data.get('worst_perimeter'),
            "mean perimeter": request.data.get('mean_perimeter'),
            "mean radius": request.data.get('mean_radius'),
            "mean area": request.data.get('mean_area'),
            "worst concavity": request.data.get('worst_concavity')
            }
            data = {'features' : request_data}
            
            # Handle dictionary input format
            if not isinstance(data, dict) or 'features' not in data:
                return Response({
                    "error": "Invalid input format",
                    "message": "Expected format: {'features': {feature_name: value, ...}}",
                    "example": {
                        "features": {
                            "worst area": 515.8,
                            "worst concave points": 0.0737,
                            # ... other features
                        }
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            features_dict = data['features']
            
            # Validate all required features are present
            missing_features = set(REQUIRED_FEATURES) - set(features_dict.keys())
            if missing_features:
                return render(request, 'dashboard.html', {
                    "error": "Missing features",
                    "missing_features": list(missing_features),
                    "required_features": REQUIRED_FEATURES
                }, status=status.HTTP_400_BAD_REQUEST)

            # Convert dictionary to ordered list based on feature importance
            features_list = [features_dict[feature] for feature in REQUIRED_FEATURES]

            # Validate numerical values
            if not all(isinstance(x, (int, float)) for x in features_list):
                return render(request, 'dashboard.html',{
                    "error": "Invalid feature values",
                    "message": "All features must be numerical values"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Make prediction
            input_data = np.array(features_list).reshape(1, -1)
            scaled_data = scaler_top.transform(input_data)
            prediction = final_model.predict(scaled_data)
            probabilities = final_model.predict_proba(scaled_data)[0]
            
            result = "malignant" if prediction[0] == 0 else "benign"
            confidence = float(probabilities[0] if result == "malignant" else probabilities[1])

            response = {
                "prediction": result,
                "confidence": round(confidence * 100, 2),
                "features_received": {
                    feature: value for feature, value in zip(REQUIRED_FEATURES, features_list)
                }
            }

            if result == "malignant":
                response.update({
                    "severity": "High Risk",
                    "message": "Please consult a doctor immediately.",
                    "recommended_actions": [
                        "Schedule immediate follow-up",
                        "Prepare medical history",
                        "Contact oncology department"
                    ]
                })
            else:
                response.update({
                    "severity": "Low Risk",
                    "message": "No immediate action required.",
                    "recommended_actions": [
                        "Continue regular check-ups",
                        "Schedule next screening as recommended"
                    ]
                })

            return render(request, 'dashboard.html', response, status=status.HTTP_200_OK)

        except Exception as e:
            return render(request, 'dashboard.html',{
                "error": "Prediction failed",
                "message": str(e),
                "required_features": REQUIRED_FEATURES
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)