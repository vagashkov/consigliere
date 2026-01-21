from src.dependencies import get_knowledge_base_loader


class KnowledgeBaseService:
    """
    LLM service implementation
    """

    def __init__(self):
        super().__init__()
        self.client = get_knowledge_base_loader()

    def load_knowledge_base(self):
        return self.client.load_knowledge_base()
