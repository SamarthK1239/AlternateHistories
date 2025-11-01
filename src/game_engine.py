"""
Game engine for managing alternate history scenarios and AI interactions.
"""

import json
from typing import Dict, List, Optional, Any
from openai import OpenAI

from .scenarios import HistoricalScenario, AVAILABLE_SCENARIOS
from .ai_client import AIClient

class GameState:
    """Represents the current state of the game."""
    
    def __init__(self, scenario: HistoricalScenario):
        self.scenario = scenario
        self.current_situation = scenario.initial_situation
        self.choices_made = []
        self.timeline_alterations = []
        self.is_complete = False

class GameEngine:
    """Main game engine that orchestrates the alternate history experience."""
    
    def __init__(self, api_key: str):
        self.ai_client = AIClient(api_key)
        self.current_state: Optional[GameState] = None
        self._active = False
        self.ui = None  # Will be set by main.py
    
    def set_ui(self, ui):
        """Set the UI reference for loading indicators."""
        self.ui = ui
    
    def start_scenario(self, scenario_name: str) -> bool:
        """Start a new scenario."""
        scenario = AVAILABLE_SCENARIOS.get(scenario_name)
        if not scenario:
            return False
        
        self.current_state = GameState(scenario)
        self._active = True
        return True
    
    def is_active(self) -> bool:
        """Check if a game is currently active."""
        return self._active and self.current_state is not None and not self.current_state.is_complete
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current game state for display."""
        if not self.current_state:
            return {}
        
        return {
            'scenario_name': self.current_state.scenario.name,
            'situation': self.current_state.current_situation,
            'choices_made': len(self.current_state.choices_made),
            'timeline_alterations': self.current_state.timeline_alterations
        }
    
    def get_available_choices(self) -> List[Dict[str, str]]:
        """Get available choices for the current situation."""
        if not self.current_state or self.current_state.is_complete:
            return []
        
        # Use AI to generate contextual choices
        prompt = self._build_choice_generation_prompt()
        
        try:
            if self.ui:
                self.ui.start_loading("Generating historical choices")
            
            response = self.ai_client.generate_choices(prompt)
            
            if self.ui:
                self.ui.stop_loading()
            
            return self._parse_ai_choices(response)
        except Exception as e:
            if self.ui:
                self.ui.stop_loading()
            # Fallback to predefined choices if AI fails
            return self._get_fallback_choices()
    
    def make_choice(self, choice_id: str) -> bool:
        """Make a choice and advance the story."""
        if not self.current_state:
            return False
        
        # Find the choice details
        available_choices = self.get_available_choices()
        chosen_option = next((choice for choice in available_choices if choice['id'] == choice_id), None)
        
        if not chosen_option:
            return False
        
        # Record the choice
        self.current_state.choices_made.append(chosen_option)
        
        # Generate consequences using AI
        consequence_prompt = self._build_consequence_prompt(chosen_option)
        
        try:
            if self.ui:
                self.ui.start_loading("Calculating historical consequences")
            
            consequence = self.ai_client.generate_consequence(consequence_prompt)
            
            if self.ui:
                self.ui.stop_loading()
            
            self.current_state.current_situation = consequence['new_situation']
            self.current_state.timeline_alterations.extend(consequence.get('alterations', []))
            
            # Check if this ends the scenario
            if consequence.get('is_ending', False):
                self.current_state.is_complete = True
            
        except Exception as e:
            if self.ui:
                self.ui.stop_loading()
            # Fallback consequence
            self.current_state.current_situation = f"Your choice to '{chosen_option['description']}' has created ripple effects through history..."
        
        return True
    
    def _build_choice_generation_prompt(self) -> str:
        """Build a prompt for AI to generate contextual choices."""
        state = self.current_state
        return f"""
        You are creating an alternate history scenario. 
        
        Historical Context: {state.scenario.name}
        Current Situation: {state.current_situation}
        Previous Choices: {[choice['description'] for choice in state.choices_made[-3:]]}
        
        Generate 3-4 plausible choices that a key decision-maker in this situation might face.
        Each choice should have the potential to significantly alter the course of history.
        
        Return the response in this exact JSON format:
        {{
            "choices": [
                {{
                    "id": "choice_1",
                    "description": "Brief description of the choice",
                    "potential_impact": "Short description of potential consequences"
                }}
            ]
        }}
        """
    
    def _build_consequence_prompt(self, choice: Dict[str, str]) -> str:
        """Build a prompt for AI to generate consequences of a choice."""
        state = self.current_state
        return f"""
        You are narrating an alternate history scenario.
        
        Historical Context: {state.scenario.name}
        Current Situation: {state.current_situation}
        Choice Made: {choice['description']}
        
        Generate the immediate and long-term consequences of this choice.
        Show how this decision ripples through history.
        
        Return the response in this exact JSON format:
        {{
            "new_situation": "Description of the new situation after the choice",
            "alterations": ["List of specific changes to the timeline"],
            "is_ending": false
        }}
        
        Set "is_ending" to true if this choice leads to a natural conclusion of the scenario.
        """
    
    def _parse_ai_choices(self, ai_response: str) -> List[Dict[str, str]]:
        """Parse AI response into choice format."""
        try:
            data = json.loads(ai_response)
            return data.get('choices', [])
        except:
            return self._get_fallback_choices()
    
    def _get_fallback_choices(self) -> List[Dict[str, str]]:
        """Provide fallback choices if AI fails."""
        return [
            {
                "id": "diplomatic",
                "description": "Pursue diplomatic negotiations",
                "potential_impact": "May lead to peaceful resolution but could show weakness"
            },
            {
                "id": "aggressive",
                "description": "Take decisive military action",
                "potential_impact": "Quick results but may escalate conflict"
            },
            {
                "id": "wait",
                "description": "Wait and gather more information",
                "potential_impact": "Safer approach but may miss opportunities"
            }
        ]