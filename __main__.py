"""Entry point for Snake Game."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    """Main function that starts the game."""
    try:
        from src.snake import run
        run()
    except ImportError as e:
        print(f"Error importing game module: {e}")
        print("Make sure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
