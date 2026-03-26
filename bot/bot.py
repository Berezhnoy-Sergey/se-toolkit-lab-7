#!/usr/bin/env python
import sys
import argparse
from handlers import commands

from dotenv import load_dotenv
load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test mode: run command and print response")
    args = parser.parse_args()
    
    if args.test:
        parts = args.test.split()
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        
        if cmd == "/start":
            print(commands.start())
        elif cmd == "/help":
            print(commands.help())
        elif cmd == "/health":
            print(commands.health())
        elif cmd == "/labs":
            print(commands.labs())
        elif cmd == "/scores" and arg:
            print(commands.scores(arg))
        elif cmd == "/scores":
            print("Usage: /scores <lab>")
        else:
            print(f"Unknown command: {cmd}. Try /help")
        return
    
    print("Bot starting... (real Telegram mode not implemented)")

if __name__ == "__main__":
    main()
