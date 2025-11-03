"""
Blackbox Integration - Anthropic Claude API Wrapper
Provides a clean interface for interacting with Claude models
"""

import os
from typing import List, Dict, Any, Optional, Generator
from anthropic import Anthropic, Stream
from anthropic.types import Message, MessageStreamEvent


class BlackboxIntegration:
    """
    Integration wrapper for Anthropic's Claude API (Blackbox)
    Provides conversation management and streaming support
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 8192,
        temperature: float = 1.0,
        system_prompt: Optional[str] = None
    ):
        """
        Initialize Blackbox integration
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            system_prompt: System prompt for the assistant
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
    
    def _default_system_prompt(self) -> str:
        """Default system prompt for Blackbox"""
        return """You are Blackbox, a helpful AI assistant integrated into a Python codebase. 
You are knowledgeable about software development, data science, AI/ML, and general programming.
You provide clear, concise, and accurate responses. When writing code, you follow best practices 
and explain your reasoning when helpful."""
    
    def chat(
        self,
        message: str,
        stream: bool = False,
        include_history: bool = True
    ) -> str | Generator[str, None, None]:
        """
        Send a message and get a response
        
        Args:
            message: User message
            stream: Whether to stream the response
            include_history: Whether to include conversation history
            
        Returns:
            Response text (or generator if streaming)
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Prepare messages for API call
        messages = self.conversation_history if include_history else [
            {"role": "user", "content": message}
        ]
        
        if stream:
            return self._stream_response(messages)
        else:
            return self._get_response(messages)
    
    def _get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get a complete response (non-streaming)"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=messages
        )
        
        # Extract text from response
        assistant_message = response.content[0].text
        
        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def _stream_response(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """Stream response chunks"""
        full_response = ""
        
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                yield text
        
        # Add complete response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": full_response
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def set_system_prompt(self, prompt: str):
        """Update system prompt"""
        self.system_prompt = prompt
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information for orchestrator"""
        return {
            "name": "Blackbox (Claude)",
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "conversation_length": len(self.conversation_history),
            "status": "active"
        }
    
    def save_conversation(self, filepath: str):
        """Save conversation history to file"""
        import json
        with open(filepath, 'w') as f:
            json.dump({
                "model": self.model,
                "system_prompt": self.system_prompt,
                "conversation": self.conversation_history
            }, f, indent=2)
    
    def load_conversation(self, filepath: str):
        """Load conversation history from file"""
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.model = data.get("model", self.model)
            self.system_prompt = data.get("system_prompt", self.system_prompt)
            self.conversation_history = data.get("conversation", [])
