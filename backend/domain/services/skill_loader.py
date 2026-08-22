import hashlib
import os

from pydantic import BaseModel


class SemanticSkillSnapshot(BaseModel):
    identity: str
    version: str
    revision_hash: str
    methodology_reference: str
    instructions: str


class SemanticSkillLoader:
    """
    Loads and snapshots the Canonical Semantic Skill for AI Runtime execution.
    """

    SKILL_PATH = "skills/lisan-semantic-extraction/SKILL.md"

    @classmethod
    def load_skill(cls, root_path: str = ".") -> SemanticSkillSnapshot | None:
        full_path = os.path.join(root_path, cls.SKILL_PATH)
        if not os.path.exists(full_path):
            return None

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        revision_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8]

        # In a real implementation we might parse YAML frontmatter.
        # Here we do a simple snapshot.
        return SemanticSkillSnapshot(
            identity="lisan-semantic-extraction",
            version="1.0",
            revision_hash=revision_hash,
            methodology_reference="Canonical Runtime Skill",
            instructions=content,
        )
