def print_tree(node, indent=0):
    if node is None:
        return
    leaf = f" '{node.token.lexeme}'" if node.token is not None else ""
    print("  " * indent + node.symbol + leaf)
    for child in node.children:
        print_tree(child, indent + 1)
