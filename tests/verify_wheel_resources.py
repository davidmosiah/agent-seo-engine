"""Verify resources in the installed distribution, not the source tree."""
from importlib.metadata import distribution
from pathlib import Path

root = Path(__file__).resolve().parents[1]
dist = distribution("agent-seo-engine")
for source, resource in (("skill/SKILL.md", "agent_seo_engine/skill/SKILL.md"), ("MIGRATION.md", "agent_seo_engine/MIGRATION.md")):
    files = {str(path): path for path in dist.files or []}
    assert resource in files, f"missing installed resource: {resource}"
    assert dist.locate_file(files[resource]).read_bytes() == (root / source).read_bytes(), resource
print("installed wheel resources match source")
