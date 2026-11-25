class ExpressionParserMixin:
    def parse_expression(self):
        raise NotImplementedError("Member 4: implement parse_expression")

    def parse_or_expression(self):
        raise NotImplementedError("Member 4: implement parse_or_expression")

    def parse_and_expression(self):
        raise NotImplementedError("Member 4: implement parse_and_expression")

    def parse_equality(self):
        raise NotImplementedError("Member 4: implement parse_equality")

    def parse_relational(self):
        raise NotImplementedError("Member 4: implement parse_relational")

    def parse_additive(self):
        raise NotImplementedError("Member 4: implement parse_additive")

    def parse_multiplicative(self):
        raise NotImplementedError("Member 4: implement parse_multiplicative")

    def parse_unary(self):
        raise NotImplementedError("Member 4: implement parse_unary")

    def parse_postfix(self):
        raise NotImplementedError("Member 4: implement parse_postfix")

    def parse_primary(self):
        raise NotImplementedError("Member 4: implement parse_primary")

    def parse_arg_list(self):
        raise NotImplementedError("Member 4: implement parse_arg_list")
