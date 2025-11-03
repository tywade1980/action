"""
Blackbox CLI - Interactive Command-Line Interface for Claude
Provides a REPL-style interface for chatting with Claude
"""

import os
import sys
from pathlib import Path
from typing import Optional
import readline  # For command history and line editing

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from master_app.integrations.blackbox_integration import BlackboxIntegration


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def disable():
        """Disable colors (for non-terminal output)"""
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''


class BlackboxCLI:
    """
    Interactive CLI for Blackbox (Claude)
    """
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the CLI
        
        Args:
            model: Claude model to use
        """
        self.model = model
        self.blackbox: Optional[BlackboxIntegration] = None
        self.running = False
        
        # Check if output is a terminal
        if not sys.stdout.isatty():
            Colors.disable()
    
    def print_banner(self):
        """Print welcome banner"""
        banner = f"""
{Colors.HEADER}{Colors.BOLD}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                  🤖 BLACKBOX CLI 🤖                       ║
║                                                           ║
║            Interactive Claude Assistant                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.OKCYAN}Model:{Colors.ENDC} {self.model}
{Colors.OKCYAN}Commands:{Colors.ENDC} Type {Colors.BOLD}/help{Colors.ENDC} for available commands

{Colors.WARNING}Ready to chat! Type your message and press Enter.{Colors.ENDC}
"""
        print(banner)
    
    def print_help(self):
        """Print help message"""
        help_text = f"""
{Colors.BOLD}Available Commands:{Colors.ENDC}

  {Colors.OKGREEN}/help{Colors.ENDC}              Show this help message
  {Colors.OKGREEN}/clear{Colors.ENDC}             Clear conversation history
  {Colors.OKGREEN}/history{Colors.ENDC}           Show conversation history
  {Colors.OKGREEN}/save <file>{Colors.ENDC}       Save conversation to file
  {Colors.OKGREEN}/load <file>{Colors.ENDC}       Load conversation from file
  {Colors.OKGREEN}/system <prompt>{Colors.ENDC}   Set system prompt
  {Colors.OKGREEN}/model <name>{Colors.ENDC}      Change model (requires restart)
  {Colors.OKGREEN}/exit{Colors.ENDC} or {Colors.OKGREEN}/quit{Colors.ENDC}    Exit the CLI

{Colors.BOLD}Tips:{Colors.ENDC}
  • Press Ctrl+C to cancel current input
  • Press Ctrl+D to exit
  • Use arrow keys for command history
  • Multi-line input: end with backslash (\\)
"""
        print(help_text)
    
    def initialize_blackbox(self):
        """Initialize Blackbox integration"""
        try:
            self.blackbox = BlackboxIntegration(model=self.model)
            return True
        except ValueError as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
            print(f"\n{Colors.WARNING}Please set your ANTHROPIC_API_KEY environment variable:{Colors.ENDC}")
            print(f"  export ANTHROPIC_API_KEY='your-api-key-here'")
            print(f"\nOr create a .env file in the project root with:")
            print(f"  ANTHROPIC_API_KEY=your-api-key-here")
            return False
    
    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands
        
        Args:
            user_input: User input string
            
        Returns:
            True if should continue, False if should exit
        """
        if not user_input.startswith('/'):
            return True
        
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in ['/exit', '/quit']:
            print(f"\n{Colors.OKCYAN}Goodbye! 👋{Colors.ENDC}\n")
            return False
        
        elif command == '/help':
            self.print_help()
        
        elif command == '/clear':
            self.blackbox.clear_history()
            print(f"{Colors.OKGREEN}✓ Conversation history cleared{Colors.ENDC}")
        
        elif command == '/history':
            history = self.blackbox.get_history()
            if not history:
                print(f"{Colors.WARNING}No conversation history{Colors.ENDC}")
            else:
                print(f"\n{Colors.BOLD}Conversation History:{Colors.ENDC}\n")
                for i, msg in enumerate(history, 1):
                    role = msg['role'].capitalize()
                    content = msg['content']
                    color = Colors.OKBLUE if role == "User" else Colors.OKGREEN
                    print(f"{color}{role}:{Colors.ENDC} {content[:100]}{'...' if len(content) > 100 else ''}\n")
        
        elif command == '/save':
            if not args:
                print(f"{Colors.FAIL}Error: Please specify a filename{Colors.ENDC}")
                print(f"Usage: /save <filename>")
            else:
                try:
                    self.blackbox.save_conversation(args)
                    print(f"{Colors.OKGREEN}✓ Conversation saved to {args}{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}Error saving conversation: {e}{Colors.ENDC}")
        
        elif command == '/load':
            if not args:
                print(f"{Colors.FAIL}Error: Please specify a filename{Colors.ENDC}")
                print(f"Usage: /load <filename>")
            else:
                try:
                    self.blackbox.load_conversation(args)
                    print(f"{Colors.OKGREEN}✓ Conversation loaded from {args}{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}Error loading conversation: {e}{Colors.ENDC}")
        
        elif command == '/system':
            if not args:
                print(f"{Colors.FAIL}Error: Please specify a system prompt{Colors.ENDC}")
                print(f"Usage: /system <prompt>")
            else:
                self.blackbox.set_system_prompt(args)
                print(f"{Colors.OKGREEN}✓ System prompt updated{Colors.ENDC}")
        
        elif command == '/model':
            if not args:
                print(f"{Colors.FAIL}Error: Please specify a model name{Colors.ENDC}")
                print(f"Usage: /model <model-name>")
                print(f"\nAvailable models:")
                print(f"  • claude-3-5-sonnet-20241022 (default)")
                print(f"  • claude-3-5-haiku-20241022")
                print(f"  • claude-3-opus-20240229")
            else:
                self.model = args
                print(f"{Colors.WARNING}Model will change to {args} on next restart{Colors.ENDC}")
                print(f"Reinitializing...")
                if self.initialize_blackbox():
                    print(f"{Colors.OKGREEN}✓ Model changed to {args}{Colors.ENDC}")
        
        else:
            print(f"{Colors.FAIL}Unknown command: {command}{Colors.ENDC}")
            print(f"Type {Colors.BOLD}/help{Colors.ENDC} for available commands")
        
        return True
    
    def get_multiline_input(self) -> Optional[str]:
        """
        Get user input (supports multi-line with backslash)
        
        Returns:
            User input string or None if interrupted
        """
        lines = []
        prompt = f"{Colors.OKBLUE}You:{Colors.ENDC} "
        
        try:
            while True:
                if lines:
                    line = input(f"{Colors.OKBLUE}...:{Colors.ENDC} ")
                else:
                    line = input(prompt)
                
                # Check if line ends with backslash (continuation)
                if line.endswith('\\'):
                    lines.append(line[:-1])  # Remove backslash
                else:
                    lines.append(line)
                    break
            
            return '\n'.join(lines).strip()
        
        except (KeyboardInterrupt, EOFError):
            return None
    
    def chat_loop(self):
        """Main chat loop"""
        self.running = True
        
        while self.running:
            try:
                # Get user input
                user_input = self.get_multiline_input()
                
                if user_input is None:
                    print(f"\n{Colors.OKCYAN}Goodbye! 👋{Colors.ENDC}\n")
                    break
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    should_continue = self.handle_command(user_input)
                    if not should_continue:
                        break
                    continue
                
                # Get response from Blackbox
                print(f"\n{Colors.OKGREEN}Blackbox:{Colors.ENDC} ", end='', flush=True)
                
                # Stream the response
                for chunk in self.blackbox.chat(user_input, stream=True):
                    print(chunk, end='', flush=True)
                
                print("\n")  # New line after response
            
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Interrupted. Type /exit to quit.{Colors.ENDC}\n")
                continue
            
            except Exception as e:
                print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}\n")
                continue
    
    def run(self):
        """Run the CLI"""
        self.print_banner()
        
        # Initialize Blackbox
        if not self.initialize_blackbox():
            return 1
        
        print(f"{Colors.OKGREEN}✓ Connected to Claude{Colors.ENDC}\n")
        
        # Start chat loop
        try:
            self.chat_loop()
        except Exception as e:
            print(f"\n{Colors.FAIL}Fatal error: {e}{Colors.ENDC}\n")
            return 1
        
        return 0


def main():
    """Main entry point for CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Blackbox CLI - Interactive Claude Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--model',
        default='claude-3-5-sonnet-20241022',
        help='Claude model to use (default: claude-3-5-sonnet-20241022)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    # Create and run CLI
    cli = BlackboxCLI(model=args.model)
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
