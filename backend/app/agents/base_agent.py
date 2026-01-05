"""
Base agent class for agentic reasoning
Inspired by STAgent's architecture
"""
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel
import json
import asyncio
from datetime import datetime


class AgentThought(BaseModel):
    """Represents a single thought/reasoning step"""
    step: int
    thought: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()


class AgentTrace(BaseModel):
    """Complete reasoning trace"""
    thoughts: List[AgentThought] = []
    final_answer: Optional[str] = None
    success: bool = False
    error: Optional[str] = None
    total_steps: int = 0
    execution_time_ms: float = 0


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(
        self,
        name: str,
        description: str,
        tools: List[Any],
        max_iterations: int = 10
    ):
        self.name = name
        self.description = description
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
    
    @abstractmethod
    async def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentTrace:
        """Run the agent on a query"""
        pass
    
    async def execute_tool(
        self,
        tool_name: str,
        tool_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool and return output"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool {tool_name} not found"
            }
        
        tool = self.tools[tool_name]
        try:
            # Convert dict to tool input model
            input_class = tool.__class__.__mro__[0]
            result = await tool.execute(tool_input)
            return result.model_dump()
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def verify_output(self, output: Dict[str, Any]) -> bool:
        """Verify tool output quality"""
        if not output.get("success"):
            return False
        
        data = output.get("data")
        if data is None:
            return False
        
        # Additional verification logic
        return True
    
    def get_tool_descriptions(self) -> str:
        """Get formatted tool descriptions"""
        descriptions = []
        for tool_name, tool in self.tools.items():
            desc = f"- {tool_name}: {tool.description}"
            descriptions.append(desc)
        return "\n".join(descriptions)
