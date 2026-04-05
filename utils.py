import os
import sys


def base_dir():
	if getattr(sys, "frozen", False):
		return os.path.dirname(sys.executable)
	return os.path.dirname(os.path.abspath(__file__))


def clear_screen():
	os.system("clear" if os.name != "nt" else "cls")


def pause():
	input("\nPress Enter to continue...")
