from abc import ABC, abstractmethod


class KnowledgeBaseLoader(ABC):
    """Abstract class for knowledge base loaders."""

    @abstractmethod
    def load_knowledge_base(self) -> str:
        pass
