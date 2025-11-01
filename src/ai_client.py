"""
AI client for interacting with OpenAI API.
"""

import json
from typing import Dict, Any
from openai import OpenAI

class AIClient:
    """Client for AI interactions."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
    
    def generate_choices(self, prompt: str) -> str:
        """Generate choices using AI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert historian and creative writer specializing in alternate history scenarios. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI choice generation failed: {e}")
    
    def generate_consequence(self, prompt: str) -> Dict[str, Any]:
        """Generate consequences using AI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert historian and creative writer specializing in alternate history scenarios. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            raise Exception(f"AI consequence generation failed: {e}")