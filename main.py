#!/usr/bin/env python3
"""
ComputerQuest - An Interactive Fiction Game about Computer Architecture

Explore a computer system from the inside while hunting for viruses
and learning about computer architecture along the way.
"""

import time
from game import Game

if __name__ == "__main__":
    try:
        # Display loading message
        print("Initializing ComputerQuest...\n")
        time.sleep(1)
        
        # Create and start game
        computer_quest = Game()
        computer_quest.start()
        
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGame terminated. Goodbye!")
    except Exception as e:
        # Log other errors
        print(f"\n\nAn error occurred: {e}")
        print("Please report this error to the developer.")
        input("Press Enter to exit...")