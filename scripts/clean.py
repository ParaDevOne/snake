#!/usr/bin/env python3
"""
Clean Script for Snake Game
Removes temporary files, caches, and build artifacts
"""

import os
import sys
import shutil
import glob
from pathlib import Path
import time

class ProjectCleaner:
    """Project cleanup utility"""
    
    def __init__(self):
        self.project_root = Path(os.path.dirname(os.path.dirname(__file__)))
        self.cleaned_files = 0
        self.cleaned_dirs = 0
        self.freed_space = 0
        
    def log(self, message, status="INFO"):
        """Log cleanup messages with status"""
        status_colors = {
            "CLEAN": "\033[92m🧹\033[0m",
            "SKIP": "\033[93m⏭\033[0m", 
            "INFO": "\033[94mℹ\033[0m",
            "WARN": "\033[93m⚠\033[0m",
            "ERROR": "\033[91m❌\033[0m"
        }
        print(f"{status_colors.get(status, status)} {message}")
    
    def get_size(self, path):
        """Get size of file or directory in bytes"""
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            total = 0
            try:
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total += os.path.getsize(filepath)
                        except (OSError, IOError):
                            pass
            except (OSError, IOError):
                pass
            return total
        return 0
    
    def format_size(self, bytes_size):
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    
    def clean_pycache(self):
        """Remove __pycache__ directories and .pyc files"""
        self.log("Cleaning Python cache files...", "INFO")
        
        # Find all __pycache__ directories
        pycache_dirs = []
        for root, dirs, files in os.walk(self.project_root):
            if '__pycache__' in dirs:
                pycache_dirs.append(os.path.join(root, '__pycache__'))
        
        # Remove __pycache__ directories
        for pycache_dir in pycache_dirs:
            try:
                size = self.get_size(pycache_dir)
                shutil.rmtree(pycache_dir)
                self.log(f"Removed: {pycache_dir} ({self.format_size(size)})", "CLEAN")
                self.cleaned_dirs += 1
                self.freed_space += size
            except Exception as e:
                self.log(f"Failed to remove {pycache_dir}: {str(e)}", "ERROR")
        
        # Find and remove .pyc files
        pyc_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.pyc'):
                    pyc_files.append(os.path.join(root, file))
        
        for pyc_file in pyc_files:
            try:
                size = self.get_size(pyc_file)
                os.remove(pyc_file)
                self.log(f"Removed: {pyc_file} ({self.format_size(size)})", "CLEAN")
                self.cleaned_files += 1
                self.freed_space += size
            except Exception as e:
                self.log(f"Failed to remove {pyc_file}: {str(e)}", "ERROR")
    
    def clean_build_artifacts(self):
        """Remove build and distribution directories"""
        self.log("Cleaning build artifacts...", "INFO")
        
        build_dirs = ['build', 'dist', '.eggs', '*.egg-info']
        
        for pattern in build_dirs:
            paths = glob.glob(str(self.project_root / pattern))
            for path in paths:
                try:
                    size = self.get_size(path)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        self.log(f"Removed directory: {path} ({self.format_size(size)})", "CLEAN")
                        self.cleaned_dirs += 1
                    else:
                        os.remove(path)
                        self.log(f"Removed file: {path} ({self.format_size(size)})", "CLEAN")
                        self.cleaned_files += 1
                    self.freed_space += size
                except Exception as e:
                    self.log(f"Failed to remove {path}: {str(e)}", "ERROR")
    
    def clean_logs(self, keep_recent=True):
        """Clean log files (optionally keep recent ones)"""
        self.log("Cleaning log files...", "INFO")
        
        log_patterns = [
            'Data/logs.txt',
            'Data/*.log',
            '*.log',
            'logs/*.log'
        ]
        
        for pattern in log_patterns:
            paths = glob.glob(str(self.project_root / pattern))
            for path in paths:
                try:
                    if keep_recent:
                        # Keep files modified in last 24 hours
                        mod_time = os.path.getmtime(path)
                        if time.time() - mod_time < 86400:  # 24 hours
                            self.log(f"Keeping recent log: {path}", "SKIP")
                            continue
                    
                    size = self.get_size(path)
                    os.remove(path)
                    self.log(f"Removed log: {path} ({self.format_size(size)})", "CLEAN")
                    self.cleaned_files += 1
                    self.freed_space += size
                except Exception as e:
                    self.log(f"Failed to remove {path}: {str(e)}", "ERROR")
    
    def clean_temp_files(self):
        """Remove temporary files"""
        self.log("Cleaning temporary files...", "INFO")
        
        temp_patterns = [
            '*.tmp',
            '*.temp',
            '*~',
            '.DS_Store',
            'Thumbs.db',
            '*.swp',
            '*.swo',
            '.coverage',
            'htmlcov/',
            '.pytest_cache/',
            '.mypy_cache/',
            '.tox/'
        ]
        
        for pattern in temp_patterns:
            paths = glob.glob(str(self.project_root / pattern))
            paths.extend(glob.glob(str(self.project_root / '**' / pattern), recursive=True))
            
            for path in paths:
                try:
                    size = self.get_size(path)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        self.log(f"Removed temp directory: {path} ({self.format_size(size)})", "CLEAN")
                        self.cleaned_dirs += 1
                    else:
                        os.remove(path)
                        self.log(f"Removed temp file: {path} ({self.format_size(size)})", "CLEAN")
                        self.cleaned_files += 1
                    self.freed_space += size
                except Exception as e:
                    self.log(f"Failed to remove {path}: {str(e)}", "ERROR")
    
    def clean_ide_files(self):
        """Remove IDE-specific files"""
        self.log("Cleaning IDE files...", "INFO")
        
        ide_patterns = [
            '.vscode/',
            '.idea/',
            '*.sublime-project',
            '*.sublime-workspace',
            '.project',
            '.pydevproject'
        ]
        
        for pattern in ide_patterns:
            paths = glob.glob(str(self.project_root / pattern))
            for path in paths:
                try:
                    size = self.get_size(path)
                    if os.path.isdir(path):
                        # Ask before removing IDE directories
                        response = input(f"Remove IDE directory {path}? (y/N): ")
                        if response.lower() == 'y':
                            shutil.rmtree(path)
                            self.log(f"Removed IDE directory: {path} ({self.format_size(size)})", "CLEAN")
                            self.cleaned_dirs += 1
                            self.freed_space += size
                        else:
                            self.log(f"Skipped IDE directory: {path}", "SKIP")
                    else:
                        os.remove(path)
                        self.log(f"Removed IDE file: {path} ({self.format_size(size)})", "CLEAN")
                        self.cleaned_files += 1
                        self.freed_space += size
                except Exception as e:
                    self.log(f"Failed to remove {path}: {str(e)}", "ERROR")
    
    def clean_all(self, include_logs=False, include_ide=False):
        """Run all cleanup operations"""
        self.log("=" * 50, "INFO")
        self.log("STARTING PROJECT CLEANUP", "INFO")
        self.log("=" * 50, "INFO")
        
        start_time = time.time()
        
        # Run cleanup operations
        self.clean_pycache()
        self.clean_build_artifacts()
        self.clean_temp_files()
        
        if include_logs:
            self.clean_logs(keep_recent=True)
        
        if include_ide:
            self.clean_ide_files()
        
        # Print summary
        self.print_summary(time.time() - start_time)
    
    def print_summary(self, duration):
        """Print cleanup summary"""
        self.log("=" * 50, "INFO")
        self.log("CLEANUP SUMMARY", "INFO")
        self.log("=" * 50, "INFO")
        self.log(f"Files removed: {self.cleaned_files}", "INFO")
        self.log(f"Directories removed: {self.cleaned_dirs}", "INFO")
        self.log(f"Space freed: {self.format_size(self.freed_space)}", "INFO")
        self.log(f"Time taken: {duration:.2f} seconds", "INFO")
        
        if self.cleaned_files > 0 or self.cleaned_dirs > 0:
            self.log("🎉 CLEANUP COMPLETED!", "CLEAN")
        else:
            self.log("✨ Project already clean!", "INFO")

def main():
    """Main cleanup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean Snake Game project")
    parser.add_argument("--logs", action="store_true", help="Include log files in cleanup")
    parser.add_argument("--ide", action="store_true", help="Include IDE files in cleanup")
    parser.add_argument("--all", action="store_true", help="Clean everything (logs + IDE)")
    
    args = parser.parse_args()
    
    cleaner = ProjectCleaner()
    
    include_logs = args.logs or args.all
    include_ide = args.ide or args.all
    
    cleaner.clean_all(include_logs=include_logs, include_ide=include_ide)

if __name__ == "__main__":
    main()
