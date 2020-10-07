import ast
import base64
from os import getcwd, path
from typing import Optional, Dict

from django.conf import settings

from apps.structure import extract_all_files_from_path


class FileReaderMixin:
    def get_study_tree(self):
        with open(self.entrypoint, "r") as source:
            tree = ast.parse(source.read())
            return tree


class Base64ContentReaderMixin:
    def get_study_tree(self):
        decoded_content = base64.b64decode(self.entrypoint)
        tree = ast.parse(decoded_content)
        return tree


class BaseAnalyzer(ast.NodeVisitor):
    def __init__(self, entrypoint: str):
        self.entrypoint = entrypoint

    def start(self):
        tree = self.get_study_tree()
        self.visit(tree)


class BaseFileAnalyzer(BaseAnalyzer, FileReaderMixin):
    pass


class BaseRawContentAnalyzer(BaseAnalyzer, Base64ContentReaderMixin):
    pass


class Analyzer(ast.NodeVisitor):
    def __init__(self, file_path: str, module: str, root_name: Optional[str] = None):
        self.root_name = root_name or settings.REPO_CLONE_PATH
        self.module = module
        self.study_file_path = file_path
        self.hits = []

    def start(self):
        full_path = path.join(getcwd(), self.root_name, self.study_file_path)
        with open(full_path, "r") as source:
            tree = ast.parse(source.read())
            self.visit(tree)

    def visit_ImportFrom(self, node):
        if node.module is not None and node.module.startswith(self.module):
            self.process_node(node)
        self.generic_visit(node)

    def process_node(self, node):
        self.hits.append(f"{self.study_file_path}:{node.lineno}")

    def hits(self):
        return self.hits


def analyze(file_path: str, module: str):
    cwd = getcwd()

    analyzer = Analyzer(file_path, module)
    analyzer.start()
    return analyzer.hits


def analyze_repo_with_pattern(pattern: str):
    hits = []
    for file_path in extract_all_files_from_path("apps",
                                                 ignore_paths=["apps/catalog", "apps/promotions", "apps/stores"]):
        hits += analyze(file_path=file_path, module=pattern)
    return hits


class FunctionMetadataAnalyzer(BaseFileAnalyzer):
    def __init__(self, entrypoint: str, context: Dict = {}):
        super(FunctionMetadataAnalyzer, self).__init__(entrypoint=entrypoint)
        self.functions = {}
        self.context = context

    def visit_FunctionDef(self, node):
        self.process_node(node)

    def process_node(self, node):
        if node.name not in self.functions:
            self.functions[node.name] = dict(count=1, **self.context)
        else:
            metadata = self.functions[node.name]
            metadata["count"] += 1
            self.functions[node.name] = metadata

    def get_analysis(self):
        return self.functions


class FunctionMetadataRawContentAnalyzer(BaseRawContentAnalyzer):
    def __init__(self, entrypoint: str, context: Dict = {}):
        super(FunctionMetadataRawContentAnalyzer, self).__init__(entrypoint=entrypoint)
        self.functions = {}
        self.context = context

    def visit_FunctionDef(self, node):
        self.process_node(node)

    def process_node(self, node):
        if node.name not in self.functions:
            self.functions[node.name] = dict(count=1, **self.context)
        else:
            metadata = self.functions[node.name]
            metadata["count"] += 1
            self.functions[node.name] = metadata

    def get_analysis(self):
        return self.functions


def analyze_functions(context: Dict, file_path: Optional[str] = None, content: Optional[str] = None):
    if file_path is None and content is None:
        raise Exception("Either supply a file_path or content")

    if file_path:
        analyzer = FunctionMetadataAnalyzer(entrypoint=file_path, context=context)
    if content:
        analyzer = FunctionMetadataRawContentAnalyzer(entrypoint=content, context=context)
    analyzer.start()
    return analyzer.get_analysis()