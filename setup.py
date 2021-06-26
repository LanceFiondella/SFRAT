#!/usr/bin/env python3
import subprocess, sys

print("Installing required libraries:\n")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
input("\nSetup complete.\n")