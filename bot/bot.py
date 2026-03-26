#!/usr/bin/env python
import sys
import argparse

def handle_start():
    return "Welcome to the LMS Bot! Use /help to see available commands."

def handle_help():
    return "/start - welcome message\n/help - this help\n/health - check backend status\n/labs - list available labs\n/scores <lab> - per-task scores"

def handle_health():
    return "Backend health check: placeholder (not yet implemented)"

def handle_labs():
    return "Available labs: lab-01, lab-02, lab-03, lab-04, lab-05, lab-06"

def handle_scores(lab=None):
    if not lab:
        return "Usage: /scores <lab> (e.g., /scores lab-04)"
    return f"Scores for {lab}: placeholder (not yet implemented)"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test mode: run command and print response")
    args = parser.parse_args()
    
    if args.test:
        parts = args.test.split()
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        
        if cmd == "/start":
            print(handle_start())
        elif cmd == "/help":
            print(handle_help())
        elif cmd == "/health":
            print(handle_health())
        elif cmd == "/labs":
            print(handle_labs())
        elif cmd == "/scores" and arg:
            print(handle_scores(arg))
        elif cmd == "/scores":
            print("Usage: /scores <lab>")
        else:
            print(f"Unknown command: {cmd}. Try /help")
        return
    
    print("Bot starting... (real Telegram mode not implemented in scaffold)")

if __name__ == "__main__":
    main()
