class StatementParserMixin:
    def parse_block(self):
        raise NotImplementedError("Member 3: implement parse_block")

    def parse_stmt_list(self):
        raise NotImplementedError("Member 3: implement parse_stmt_list")

    def parse_statement(self):
        raise NotImplementedError("Member 3: implement parse_statement")

    def parse_if_stmt(self):
        raise NotImplementedError("Member 3: implement parse_if_stmt")

    def parse_while_stmt(self):
        raise NotImplementedError("Member 3: implement parse_while_stmt")

    def parse_for_stmt(self):
        raise NotImplementedError("Member 3: implement parse_for_stmt")

    def parse_return_stmt(self):
        raise NotImplementedError("Member 3: implement parse_return_stmt")

    def parse_var_decl(self):
        raise NotImplementedError("Member 3: implement parse_var_decl")

    def parse_assign_stmt(self):
        raise NotImplementedError("Member 3: implement parse_assign_stmt")

    def parse_expr_stmt(self):
        raise NotImplementedError("Member 3: implement parse_expr_stmt")

    def parse_for_init(self):
        raise NotImplementedError("Member 3: implement parse_for_init")

    def parse_for_update(self):
        raise NotImplementedError("Member 3: implement parse_for_update")
