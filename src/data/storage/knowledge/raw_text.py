from pathlib import Path

from src.data.storage.knowledge.base import KnowledgeBaseLoader


class RawTextLoader(KnowledgeBaseLoader):
    """Load knowledge from markdown and text files into a single string."""

    SUPPORTED_EXTENSIONS = {".txt", ".md"}

    def __init__(self, knowledge_path: Path):
        self.knowledge_path = knowledge_path

    def _get_files_list(self, knowledge_path: Path):
        return [
            path for path in knowledge_path.rglob('*')
            if path.is_file() and path.suffix in self.SUPPORTED_EXTENSIONS
        ]

    def _load_files_content(self):
        """Load all knowledge files."""
        if not self.knowledge_path.exists():
            print(
                "Knowledge path not found: {}".format(
                    self.knowledge_path
                )
            )
            return

        documents = []

        # Walk through all subdirectories
        for knowledge_file in self._get_files_list(self.knowledge_path):
            try:
                with open(knowledge_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Add file header
                    rel_path = knowledge_file.relative_to(self.knowledge_path)
                    documents.append(f"=== {rel_path} ===\n\n{content}")
            except Exception as e:
                print(f"Warning: Failed to load {knowledge_file}: {e}")

        if documents:
            files_content = "\n\n---\n\n".join(documents)
            print(f"Loaded {len(documents)} knowledge documents")
            return files_content
        else:
            print("No knowledge documents found")
            return ""

    def load_knowledge_base(self) -> str:
        """Get all knowledge content."""
        return self._load_files_content()
