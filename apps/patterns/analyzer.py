import ast
import base64
from os import getcwd, path
from typing import Optional, Dict, List

from django.conf import settings

from apps.structure import extract_all_files_from_path


# Inputs mixin
class FileReaderMixin:
    def get_study_tree(self, entrypoint: str):
        with open(entrypoint, "r") as source:
            tree = ast.parse(source.read())
            return tree


class RawContentReaderMixin:
    def get_study_tree(self):
        tree = ast.parse(self.entrypoint)
        return tree
    

class Base64ContentReaderMixin:
    def get_study_tree(self):
        decoded_content = base64.b64decode(self.entrypoint)
        tree = ast.parse(decoded_content)
        return tree


# Absolute bare bones Analyzer class.
# Only class attributes here
class BaseAnalyzer(ast.NodeVisitor):
    def __init__(self, entrypoint: str):
        self.entrypoint = entrypoint


# Base Analyzers, per input type
class BaseFileAnalyzer(FileReaderMixin, BaseAnalyzer):
    def __init__(self, *args, **kwargs):
        super(BaseFileAnalyzer, self).__init__(*args, **kwargs)
        
    def start(self, entrypoint: Optional[str] = None):
        entrypoint = entrypoint or self.entrypoint
        
        tree = self.get_study_tree(entrypoint=entrypoint)
        self.visit(tree)


class BaseRawContentAnalyzer(RawContentReaderMixin, BaseAnalyzer):
    def __init__(self, *args, **kwargs):
        super(BaseRawContentAnalyzer, self).__init__(*args, **kwargs)

    def start(self):
        tree = self.get_study_tree()
        self.visit(tree)


class Base64RawContentAnalyzer(Base64ContentReaderMixin, BaseRawContentAnalyzer):
    pass


class Analyzer(BaseFileAnalyzer):
    def __init__(self, entrypoint: str, pattern: str, root_name: Optional[str] = None):
        self.root_name = root_name or settings.REPO_CLONE_PATH
        self.pattern = pattern
        self.hits = []
        super(Analyzer, self).__init__(entrypoint=entrypoint)

    def start(self):
        full_path = path.join(getcwd(), self.root_name, self.entrypoint)
        super(Analyzer, self).start(entrypoint=full_path)

    def visit_ImportFrom(self, node):
        if node.module is not None and node.module.startswith(self.pattern):
            self.process_node(node)
        self.generic_visit(node)

    def process_node(self, node):
        self.hits.append(f"{self.entrypoint}:{node.lineno}")

    def hits(self):
        return self.hits


def analyze(file_path: str, pattern: str):
    analyzer = Analyzer(entrypoint=file_path, pattern=pattern)
    analyzer.start()
    return analyzer.hits


def analyze_repo_with_pattern(pattern: str, ignore_paths: List[str] = []):
    hits = []
    for file_path in extract_all_files_from_path("apps",
                                                 ignore_paths=ignore_paths):
        hits += analyze(file_path=file_path, pattern=pattern)
    return hits


class FunctionMetadataAnalyzer(BaseFileAnalyzer):
    def __init__(self, *args, **kwargs):
        self.functions = {}
        self.context = kwargs.pop('context', {})
        super(FunctionMetadataAnalyzer, self).__init__(*args, **kwargs)

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


class FunctionMetadataBase64ContentAnalyzer(Base64RawContentAnalyzer):
    def __init__(self, *args, **kwargs):
        self.functions = {}
        self.context = kwargs.pop('context', {})
        super(FunctionMetadataBase64ContentAnalyzer, self).__init__(*args, **kwargs)

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
        analyzer = FunctionMetadataBase64ContentAnalyzer(entrypoint=content, context=context)
    analyzer.start()
    return analyzer.get_analysis()

