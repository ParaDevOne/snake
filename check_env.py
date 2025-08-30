"""Script to check Python environment and installed packages."""
import sys
import os
import subprocess

def main():
    print("=== Python Environment Check ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Current working directory: {os.getcwd()}")
    
    print("\n=== System Path ===")
    for i, path in enumerate(sys.path):
        print(f"{i}: {path}")
    
    print("\n=== Installed Packages ===")
    try:
        import pkg_resources
        installed_packages = sorted([f"{d.project_name}=={d.version}" for d in pkg_resources.working_set])
        for i, pkg in enumerate(installed_packages):
            print(f"{i+1}. {pkg}")
    except ImportError:
        print("Could not import pkg_resources. Trying pip list...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "list"], check=True)
        except Exception as e:
            print(f"Error running pip list: {e}")
    
    print("\n=== Pygame Check ===")
    try:
        import pygame
        print(f"Pygame version: {pygame.version.ver}")
        print(f"Pygame SDL version: {'.'.join(str(x) for x in pygame.version.SDL)}")
    except ImportError as e:
        print(f"Pygame import error: {e}")
    except Exception as e:
        print(f"Error checking Pygame: {e}")

if __name__ == "__main__":
    main()
