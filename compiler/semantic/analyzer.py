from compiler.semantic.symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, tree):
        raise NotImplementedError("Member 5: implement analyze")
