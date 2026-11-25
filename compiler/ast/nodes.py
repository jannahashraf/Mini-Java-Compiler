from dataclasses import dataclass, field
from typing import List, Optional

from compiler.tokens import Token


@dataclass
class ParseTreeNode:
    symbol: str
    token: Optional[Token] = None
    children: List["ParseTreeNode"] = field(default_factory=list)

    def add(self, child: "ParseTreeNode") -> "ParseTreeNode":
        self.children.append(child)
        return child
