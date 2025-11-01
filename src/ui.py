"""
Console user interface for the alternate history application.
"""

import os
import time
import threading
from typing import Dict, List, Optional
from colorama import Fore, Back, Style

from .scenarios import get_scenario_list

class ConsoleUI:
    """Console-based user interface."""
    
    def __init__(self):
        self.width = 80
        self._loading = False
        self._loading_thread = None
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def start_loading(self, message: str = "Consulting the AI oracle"):
        """Start displaying a loading indicator."""
        self._loading = True
        self._loading_thread = threading.Thread(target=self._show_loading_animation, args=(message,))
        self._loading_thread.daemon = True
        self._loading_thread.start()
    
    def stop_loading(self):
        """Stop the loading indicator."""
        self._loading = False
        if self._loading_thread:
            self._loading_thread.join(timeout=0.5)
        # Clear the loading line
        print(f"\r{' ' * (self.width)}\r", end='', flush=True)
    
    def _show_loading_animation(self, message: str):
        """Show animated loading indicator."""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        dots = ""
        spinner_idx = 0
        
        while self._loading:
            # Cycle through spinner characters
            spinner = spinner_chars[spinner_idx % len(spinner_chars)]
            spinner_idx += 1
            
            # Cycle dots
            dots = "." * ((len(dots) % 3) + 1)
            
            # Display loading message
            loading_text = f"{Fore.YELLOW}{spinner} {message}{dots}{Style.RESET_ALL}"
            print(f"\r{loading_text:<{self.width-1}}", end='', flush=True)
            
            time.sleep(0.1)
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{Fore.CYAN}{'=' * self.width}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{title.center(self.width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * self.width}{Style.RESET_ALL}\n")
    
    def print_separator(self):
        """Print a section separator."""
        print(f"{Fore.BLUE}{'-' * self.width}{Style.RESET_ALL}")
    
    def welcome_screen(self):
        """Display the welcome screen."""
        self.clear_screen()
        self.print_header("ALTERNATE HISTORIES EXPLORER")
        
        print(f"{Fore.YELLOW}Welcome to the Alternate Histories Explorer!{Style.RESET_ALL}")
        print()
        print("Explore pivotal moments in history and discover how different choices")
        print("could have changed the course of human civilization.")
        print()
        print(f"{Fore.GREEN}• Choose from historical scenarios{Style.RESET_ALL}")
        print(f"{Fore.GREEN}• Make decisions at crucial turning points{Style.RESET_ALL}")
        print(f"{Fore.GREEN}• See how your choices reshape history{Style.RESET_ALL}")
        print()
        input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    def select_scenario(self) -> Optional[str]:
        """Let user select a scenario."""
        while True:
            self.clear_screen()
            self.print_header("SELECT A HISTORICAL SCENARIO")
            
            scenarios = get_scenario_list()
            
            print(f"{Fore.YELLOW}Available scenarios:{Style.RESET_ALL}\n")
            
            scenario_keys = list(scenarios.keys())
            for i, (key, description) in enumerate(scenarios.items(), 1):
                print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {description}")
                print()
            
            print(f"{Fore.RED}{len(scenarios) + 1}.{Style.RESET_ALL} Exit application")
            
            self.print_separator()
            
            try:
                choice = input(f"\n{Fore.CYAN}Enter your choice (1-{len(scenarios) + 1}): {Style.RESET_ALL}").strip()
                
                if not choice.isdigit():
                    continue
                
                choice_num = int(choice)
                
                if choice_num == len(scenarios) + 1:
                    return None  # Exit
                elif 1 <= choice_num <= len(scenarios):
                    return scenario_keys[choice_num - 1]
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                    input("Press Enter to continue...")
                    
            except (ValueError, KeyboardInterrupt):
                continue
    
    def display_situation(self, state: Dict):
        """Display the current situation."""
        self.clear_screen()
        self.print_header(f"SCENARIO: {state.get('scenario_name', 'Unknown').upper()}")
        
        print(f"{Fore.YELLOW}Current Situation:{Style.RESET_ALL}")
        print()
        
        # Wrap text for better readability
        situation = state.get('situation', '')
        self._print_wrapped_text(situation)
        
        print()
        
        if state.get('timeline_alterations'):
            print(f"{Fore.MAGENTA}Timeline Alterations:{Style.RESET_ALL}")
            for i, alteration in enumerate(state['timeline_alterations'], 1):
                print(f"{Fore.BLUE}  {i}. {alteration}{Style.RESET_ALL}")
            print()
        
        choices_made = state.get('choices_made', 0)
        if choices_made > 0:
            print(f"{Fore.GREEN}Decisions made so far: {choices_made}{Style.RESET_ALL}")
            print()
    
    def get_user_choice(self, choices: List[Dict[str, str]]) -> Optional[str]:
        """Get user's choice from available options."""
        if not choices:
            return None
        
        self.print_separator()
        print(f"{Fore.YELLOW}What do you choose?{Style.RESET_ALL}\n")
        
        for i, choice in enumerate(choices, 1):
            print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {choice['description']}")
            if choice.get('potential_impact'):
                print(f"   {Fore.BLUE}→ {choice['potential_impact']}{Style.RESET_ALL}")
            print()
        
        print(f"{Fore.RED}{len(choices) + 1}.{Style.RESET_ALL} Return to scenario selection")
        
        while True:
            try:
                choice_input = input(f"\n{Fore.CYAN}Enter your choice (1-{len(choices) + 1}): {Style.RESET_ALL}").strip()
                
                if not choice_input.isdigit():
                    continue
                
                choice_num = int(choice_input)
                
                if choice_num == len(choices) + 1:
                    return None  # Go back
                elif 1 <= choice_num <= len(choices):
                    return choices[choice_num - 1]['id']
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                    
            except (ValueError, KeyboardInterrupt):
                continue
    
    def display_ending(self, state: Dict):
        """Display the ending of a scenario."""
        self.print_separator()
        print(f"\n{Fore.YELLOW}SCENARIO COMPLETE{Style.RESET_ALL}\n")
        
        print("Your choices have led to this conclusion:")
        print()
        self._print_wrapped_text(state.get('situation', ''))
        
        if state.get('timeline_alterations'):
            print(f"\n{Fore.MAGENTA}Final Timeline Changes:{Style.RESET_ALL}")
            for i, alteration in enumerate(state['timeline_alterations'], 1):
                print(f"{Fore.BLUE}  {i}. {alteration}{Style.RESET_ALL}")
        
        print()
        input(f"{Fore.MAGENTA}Press Enter to return to scenario selection...{Style.RESET_ALL}")
    
    def goodbye_screen(self):
        """Display goodbye message."""
        self.clear_screen()
        self.print_header("THANK YOU FOR EXPLORING")
        
        print(f"{Fore.YELLOW}Thank you for exploring alternate histories!{Style.RESET_ALL}")
        print()
        print("Remember: Every choice we make shapes the future.")
        print("History is not just what happened, but what could have been.")
        print()
        print(f"{Fore.GREEN}Goodbye, time traveler!{Style.RESET_ALL}")
        print()
    
    def _print_wrapped_text(self, text: str, indent: int = 0):
        """Print text wrapped to console width."""
        words = text.split()
        current_line = " " * indent
        
        for word in words:
            if len(current_line) + len(word) + 1 <= self.width - indent:
                if current_line.strip():
                    current_line += " "
                current_line += word
            else:
                print(current_line)
                current_line = " " * indent + word
        
        if current_line.strip():
            print(current_line)