# app/utils/performance_profiler.py
import ast

def detect_performance_issues(code: str) -> list[str]:
    issues = []

    try:
        tree = ast.parse(code)

        class LoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.nested_loop_depth = 0
                self.max_depth = 0

            def visit_For(self, node):
                self.nested_loop_depth += 1
                self.max_depth = max(self.max_depth, self.nested_loop_depth)
                self.generic_visit(node)
                self.nested_loop_depth -= 1

            def visit_While(self, node):
                self.nested_loop_depth += 1
                self.max_depth = max(self.max_depth, self.nested_loop_depth)
                self.generic_visit(node)
                self.nested_loop_depth -= 1

        visitor = LoopVisitor()
        visitor.visit(tree)

        if visitor.max_depth >= 3:
            issues.append("⚠️ Deeply nested loops detected. Consider refactoring for better performance.")

        for node in ast.walk(tree):
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                        if child.func.attr == "append":
                            issues.append("💡 Consider using list comprehension instead of append inside a loop.")
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        if child.func.id in ("sorted", "sort"):
                            issues.append("⚠️ Avoid sorting inside loops unless necessary.")

    except SyntaxError:
        issues.append("❌ Unable to analyze performance due to syntax errors.")

    return issues
