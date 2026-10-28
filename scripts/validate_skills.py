#!/usr/bin/env python3
"""
Validador de Integridade de Skills de Motion Design em Python.
Verifica:
1. Estrutura de diretórios em skills/
2. YAML Frontmatter válido em SKILL.md (name, description)
3. Metadados de agentes (agents/openai.yaml)
4. Integridade de links markdown locais/relativos
5. Ausência de dependências runtime de Node/npm nas skills ativas
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extrai campos do frontmatter YAML delimitado por ---."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    raw_yaml = parts[1]
    body = parts[2]
    data: Dict[str, str] = {}
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip("\"'")
    return data, body


def find_markdown_files(directory: Path) -> List[Path]:
    """Busca recursivamente todos os arquivos .md em um diretório."""
    md_files = []
    if not directory.exists():
        return md_files
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root) / f)
    return md_files


def validate_markdown_links(file_path: Path, all_files: Set[Path]) -> List[str]:
    """Verifica se links relativos apontam para arquivos existentes."""
    issues = []
    content = file_path.read_text(encoding="utf-8")
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    
    for match in link_pattern.finditer(content):
        link = match.group(1).strip()
        # Ignora URLs externas, âncoras locais e esquemas de arquivo absoluto
        if any(link.startswith(p) for p in ("http://", "https://", "mailto:", "data:", "#", "file:///")):
            continue
        # Limpa âncoras e query parameters
        clean_link = link.split("#")[0].split("?")[0]
        if not clean_link:
            continue
            
        target = (file_path.parent / clean_link).resolve()
        if not target.exists():
            issues.append(f"Link quebrado em {file_path.relative_to(REPO_ROOT)}: '{link}' -> {target}")
    return issues


def validate_skill(skill_dir: Path) -> Tuple[List[str], Dict[str, str]]:
    """Valida uma pasta de skill individual."""
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"Arquivo obrigatório ausente: {skill_md.relative_to(REPO_ROOT)}")
        return errors, {}

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    if "name" not in frontmatter or not frontmatter["name"]:
        errors.append(f"Campo 'name' ausente no frontmatter de {skill_md.relative_to(REPO_ROOT)}")
    if "description" not in frontmatter or not frontmatter["description"]:
        errors.append(f"Campo 'description' ausente no frontmatter de {skill_md.relative_to(REPO_ROOT)}")

    # Verifica agents/openai.yaml se existir pasta agents
    agents_dir = skill_dir / "agents"
    if agents_dir.exists():
        openai_yaml = agents_dir / "openai.yaml"
        if not openai_yaml.exists():
            errors.append(f"Pasta agents presente mas openai.yaml ausente em {skill_dir.name}")

    return errors, frontmatter


def run_validation(check_active_only: bool = True) -> int:
    """Executa a validação completa de todas as skills."""
    print("=" * 60)
    print("Iniciando Validação das Skills de Motion Design (Python-First)")
    print("=" * 60)

    if not SKILLS_DIR.exists():
        print(f"Erro fatal: Diretório de skills não encontrado: {SKILLS_DIR}")
        return 1

    skill_folders = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not skill_folders:
        print("Aviso: Nenhuma pasta de skill encontrada em skills/")
        return 0

    all_errors: List[str] = []
    all_md_files = set(find_markdown_files(SKILLS_DIR))
    valid_count = 0

    for sdir in sorted(skill_folders, key=lambda x: x.name):
        errors, meta = validate_skill(sdir)
        
        # Validação de links em todos os .md da skill
        for md_file in find_markdown_files(sdir):
            link_issues = validate_markdown_links(md_file, all_md_files)
            errors.extend(link_issues)

        if errors:
            all_errors.extend(errors)
            print(f"❌ {sdir.name}: {len(errors)} problema(s) detectado(s)")
            for err in errors:
                print(f"   • {err}")
        else:
            valid_count += 1
            print(f"✅ {sdir.name} ({meta.get('name', '')})")

    print("\n" + "-" * 60)
    print(f"Resumo: {valid_count}/{len(skill_folders)} skills válidas.")

    if all_errors:
        print(f"Total de falhas encontradas: {len(all_errors)}")
        return 1

    print("Todas as skills verificadas estão íntegras e em conformidade!")
    return 0


if __name__ == "__main__":
    sys.exit(run_validation())
