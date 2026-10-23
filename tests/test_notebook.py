"""Lightweight smoke tests for CS221_Final_Project.ipynb.

The notebook targets Google Colab and runs expensive experiments, so these tests
never execute it. Instead they check that it is valid JSON, that every code cell
compiles, and that every name the code reads is a builtin, imported, or defined
somewhere in the notebook. Only pytest is required.
"""

import ast
import builtins
import json
import re
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "CS221_Final_Project.ipynb"
DATASET = ROOT / "imperfect_maze.zip"

# Names provided by the Jupyter/IPython runtime rather than by Python itself.
NOTEBOOK_GLOBALS = {"get_ipython", "In", "Out"}

COLAB_IMPORT = re.compile(r"google\.colab")
# files.upload()/files.download(...) calls; replaced by None so that
# `uploaded = files.upload()` still binds `uploaded`.
COLAB_CALL = re.compile(r"\bfiles\.(upload|download)\([^)]*\)")


def load_notebook(path=NOTEBOOK):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def clean_source(source):
    """Return cell source with Colab-only code and shell/magic lines neutralized.

    `google.colab` imports and `!`/`%` lines become `pass` (keeping indentation,
    so blocks stay valid and line numbers still match the notebook), and
    `files.upload()`/`files.download(...)` calls become `None`.
    """
    lines = []
    for line in source.splitlines():
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith(("!", "%")) or COLAB_IMPORT.search(stripped):
            lines.append(f"{indent}pass")
        else:
            lines.append(COLAB_CALL.sub("None", line))
    return "\n".join(lines) + "\n"


def code_cells(nb):
    cells = []
    for index, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)
        cells.append((index, clean_source(source)))
    return cells


def bound_names(tree):
    """Every name bound anywhere in the tree (imports, defs, args, targets)."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                names.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            names.update(node.names)
    return names


def loaded_names(tree):
    return {
        (node.id, node.lineno)
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def undefined_names(nb):
    trees = [(i, ast.parse(src, filename=f"cell {i}")) for i, src in code_cells(nb)]
    known = set(dir(builtins)) | NOTEBOOK_GLOBALS
    for _, tree in trees:
        known |= bound_names(tree)
    missing = {}
    for i, tree in trees:
        for name, lineno in loaded_names(tree):
            if name not in known:
                missing.setdefault(name, []).append(f"cell {i} line {lineno}")
    return missing


def test_notebook_is_valid_json():
    nb = load_notebook()
    assert nb["nbformat"] == 4
    assert isinstance(nb["cells"], list) and nb["cells"]
    for cell in nb["cells"]:
        assert cell["cell_type"] in {"code", "markdown", "raw"}
        assert "source" in cell


def test_code_cells_compile():
    nb = load_notebook()
    cells = code_cells(nb)
    assert cells, "notebook has no code cells"
    for index, source in cells:
        compile(source, f"<cell {index}>", "exec")


def test_all_names_are_defined_or_imported():
    missing = undefined_names(load_notebook())
    assert not missing, f"names used but never imported or defined: {missing}"


def test_dataset_zip_has_mazes():
    with zipfile.ZipFile(DATASET) as zf:
        assert zf.testzip() is None
        names = [n for n in zf.namelist() if not n.startswith("__MACOSX")]
    mazes = [n for n in names if n.startswith("imperfect_maze/") and not n.endswith("/")]
    assert mazes, "no files under imperfect_maze/ in imperfect_maze.zip"
    assert any(n.endswith(".txt") for n in mazes)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
