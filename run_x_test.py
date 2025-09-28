#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to the project directory
os.chdir('/Users/a0g11b6/Desktop/InterviewPrep/SysDesignGemini')

# Run the X Twitter Thread test
try:
    result = subprocess.run([sys.executable, 'app/test_x_twitter_thread_simple.py'], 
                          capture_output=True, text=True, cwd=os.getcwd())
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Return code: {result.returncode}")
    
except Exception as e:
    print(f"Error running test: {e}")