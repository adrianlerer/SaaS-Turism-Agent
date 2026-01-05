"""
Base tool interface for agents
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ToolInput(BaseModel):
    """Base input for tools"""
    pass


class ToolOutput(BaseModel):
    """Base output for tools"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseTool(ABC):
    """Base class for all tools"""
    
    name: str
    description: str
    
    def __init__(self):
        if not hasattr(self, 'name'):
            self.name = self.__class__.__name__
        if not hasattr(self, 'description'):
            self.description = "No description provided"
    
    @abstractmethod
    async def execute(self, input_data: ToolInput) -> ToolOutput:
        """Execute the tool with given input"""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for agent"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_input_schema()
        }
    
    @abstractmethod
    def get_input_schema(self) -> Dict[str, Any]:
        """Get input schema"""
        pass
