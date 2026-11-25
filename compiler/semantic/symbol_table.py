class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, symbol):
        raise NotImplementedError("Member 5: implement declare")

    def lookup(self, name):
        raise NotImplementedError("Member 5: implement lookup")
