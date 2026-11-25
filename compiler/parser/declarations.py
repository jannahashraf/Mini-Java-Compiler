class DeclarationParserMixin:
    def parse_program(self):
        raise NotImplementedError("Member 2: implement parse_program")

    def parse_class_decl(self):
        raise NotImplementedError("Member 2: implement parse_class_decl")

    def parse_member_list(self):
        raise NotImplementedError("Member 2: implement parse_member_list")

    def parse_member(self):
        raise NotImplementedError("Member 2: implement parse_member")

    def parse_field_decl(self):
        raise NotImplementedError("Member 2: implement parse_field_decl")

    def parse_method_decl(self):
        raise NotImplementedError("Member 2: implement parse_method_decl")

    def parse_method_name(self):
        raise NotImplementedError("Member 2: implement parse_method_name")

    def parse_return_type(self):
        raise NotImplementedError("Member 2: implement parse_return_type")

    def parse_modifiers(self):
        raise NotImplementedError("Member 2: implement parse_modifiers")

    def parse_type(self):
        raise NotImplementedError("Member 2: implement parse_type")

    def parse_param_list(self):
        raise NotImplementedError("Member 2: implement parse_param_list")
