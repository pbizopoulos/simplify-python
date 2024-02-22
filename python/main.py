from __future__ import annotations

import ast
import unittest
from pathlib import Path
from shutil import copyfile
from typing import Any


class Transformer(ast.NodeTransformer):
    def visit(self: Transformer, node: Any) -> Any:  # noqa: ANN401
        self.generic_visit(node)
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant):
                return None
            if isinstance(node.value, ast.Call):  # noqa: SIM102
                if hasattr(node.value.func, "id") and node.value.func.id == "print":
                    return None
        if isinstance(node, ast.FunctionDef):
            node.returns = None
            if node.args.args:
                for arg in node.args.args:
                    arg.annotation = None
            return node
        return node


def simplify_python(code_input: str | bytes) -> str | bytes | None:
    if isinstance(code_input, str):
        with Path(code_input).open() as file:
            root = ast.parse(file.read())
    else:
        root = ast.parse(code_input.decode())
    transformer = Transformer()
    ast.fix_missing_locations(transformer.visit(root))
    code_unparsed = ast.unparse(root)
    if isinstance(code_input, str):
        with Path(code_input).open("w") as file:
            file.write(code_unparsed)
        return None
    return code_unparsed.encode()


class Tests(unittest.TestCase):
    def test_simplify_python_bytes_input(self: Tests) -> None:
        with Path("prm/before.py").open(encoding="utf-8") as file:
            code_output_before = simplify_python(file.read().encode())
        with Path("prm/after.py").open(encoding="utf-8") as file:
            code_output_after = file.read()
        if code_output_before.decode() != code_output_after:  # type: ignore[union-attr]
            raise AssertionError

    def test_simplify_python_file_input(self: Tests) -> None:
        copyfile("prm/before.py", "tmp/before_processed.py")
        simplify_python("tmp/before_processed.py")
        with Path("tmp/before_processed.py").open(encoding="utf-8") as file:
            code_output_before_processed = file.read()
        with Path("prm/after.py").open(encoding="utf-8") as file:
            code_output_after = file.read()
        if code_output_before_processed != code_output_after:
            raise AssertionError


def main() -> None:
    import fire

    fire.Fire(simplify_python)


if __name__ == "__main__":
    unittest.main()
