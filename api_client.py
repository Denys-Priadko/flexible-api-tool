#!/usr/bin/env python3
"""
CODE100 API Client
Handles JWT authentication and puzzle retrieval
"""
import requests
import json
import time
from typing import Dict, Any, Optional

def mask_token(token: str) -> str:
    """Mask token for safe display on screen"""
    if not token or len(token) <= 10:
        return token
    return token[:5] + '*' * (len(token) - 10) + token[-5:]

class CC:
    def __init__(self):
        # Customizable endpoints - update these based on actual API
        # self.base_url = "https://api.code100.dev"
        self.base_url = "https://challenger.code100.dev"
        self.auth_url = '/login'          # might be /auth, /token, etc
        self.get_p_url = '/getpuzzle'     # might be /puzzle, /challenge, etc
        self.submit_url = '/postanswer'   # might be /submit, /answer, etc
        self.user_al = 'email'            # might be 'username', 'user_id', etc
        self.password_al = 'password'     # might be 'pass', 'secret', etc
        self.solution_al = 'answer' # None #'solution'    
        self.un = ''
        self.pw = ''
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        self.submit_headers = {"Content-Type": "application/json"}
        # self.submit_headers = {"Content-Type": "text/plain"}
        self.last_response = None  # Keep last response for debugging
        
    def auth(self):
        try:
            response = requests.post(
                f"{self.base_url}{self.auth_url}",
                json={self.user_al: self.un, self.password_al: self.pw},
                headers=self.headers
            )
            self.last_response = response
            if response.status_code == 200:
                self.token = response.json().get("token")
                self.headers["Authorization"] = f"Bearer {self.token}"
                self.submit_headers["Authorization"] = f"Bearer {self.token}"

                print(f"✓ Authenticated! Token: {mask_token(self.token)}")
                return True
            else:
                print(f"Auth failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Auth failed: {e}")
            self.last_response = None
        return False

    
    def get_puzzle(self):
        if not self.token:
            print("Not authenticated")
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}{self.get_p_url}",
                headers=self.headers
            )
            self.last_response = response
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Get puzzle failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to get puzzle: {e}")
            self.last_response = None
        return None
   
    def submit(self, solution):
        """Submit solution to CODE100 API"""
        if not self.token:
            print("Not authenticated")
            return False
            
        try:
            # Build submission payload using alias
            if self.solution_al:
                payload = {self.solution_al: solution}
            else:
                # If solution_al is empty/None, send raw value
                payload = solution
            
            response = requests.post(
                f"{self.base_url}{self.submit_url}",
                json=payload,
                headers=self.submit_headers
            )
            self.last_response = response
            if response.status_code == 200:
                result = response.json()
                print(f"Submission result: {result}")
                return True
            else:
                print(f"Submit failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Submit failed: {e}")
            self.last_response = None
        return False
    
    def debug(self):
        """Print debug info about last request"""
        if not self.last_response:
            print("No response stored")
            return
            
        r = self.last_response
        print(f"=== Last Request Debug ===")
        print(f"URL: {r.url}")
        print(f"Status: {r.status_code}")
        
        # Mask Authorization header
        headers = dict(r.request.headers)
        if 'Authorization' in headers and headers['Authorization'].startswith('Bearer '):
            token = headers['Authorization'][7:]
            headers['Authorization'] = f"Bearer {mask_token(token)}"
        print(f"Headers sent: {headers}")
        
        print(f"Body sent: {r.request.body}")
        print(f"Response headers: {dict(r.headers)}")
        
        # Mask token in response text if present
        response_text = r.text
        if self.token and self.token in response_text:
            response_text = response_text.replace(self.token, mask_token(self.token))
        print(f"Response text: {response_text}")
        print("========================")

# Quick test client
'abc'.rsplit()
s = str([1,2,3])
eval(s)
json.loads(s)




