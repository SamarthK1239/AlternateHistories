"""
Main entry point for the Alternate Histories console application.
"""

import os
import sys
from dotenv import load_dotenv
from colorama import init, Fore, Style

from src.game_engine import GameEngine
from src.ui import ConsoleUI

def main():
    """Main function to run the alternate histories application."""
    
    # Initialize colorama for cross-platform colored output
    init()
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(f"{Fore.RED}Error: OpenAI API key not found!{Style.RESET_ALL}")
        print("Please:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run the application again")
        sys.exit(1)
    
    # Initialize the game engine and UI
    try:
        game_engine = GameEngine(api_key)
        ui = ConsoleUI()
        
        # Connect UI to game engine for loading indicators
        game_engine.set_ui(ui)
        
        # Start the application
        ui.welcome_screen()
        
        while True:
            scenario = ui.select_scenario()
            if scenario is None:  # User chose to exit
                break
                
            game_engine.start_scenario(scenario)
            
            while game_engine.is_active():
                current_state = game_engine.get_current_state()
                ui.display_situation(current_state)
                
                choices = game_engine.get_available_choices()
                if not choices:
                    ui.display_ending(current_state)
                    break
                
                choice = ui.get_user_choice(choices)
                if choice is None:  # User chose to go back
                    break
                    
                game_engine.make_choice(choice)
        
        ui.goodbye_screen()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Application interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()