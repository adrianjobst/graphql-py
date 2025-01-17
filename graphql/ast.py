from anytree import NodeMixin, PreOrderIter

class Node(NodeMixin):
    def __str__(self):
        arguments = []
        if hasattr(self, 'arguments'):
            for arg in self.arguments:
                arguments.append(f'{arg.name}: {arg.value}')

        return u'<%s%s%s%s>' % (
            f'{self.alias}:' if hasattr(self, 'alias') and self.alias else '',
            self.__class__.__name__,
            f' {self.name}' if hasattr(self, 'name') and self.name else '',
            '(%s)' % ', '.join(arguments) if arguments else ''
        )

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for k, v in self.__dict__.items():
            if isinstance(v, (list, tuple)) and not k=='arguments':
                continue
            if getattr(other, k) != v:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def is_paginated(self) -> bool:
        if hasattr(self, 'arguments'):
            for arg in self.arguments:
                if arg.name == 'first':
                    return True

        return False

    @property
    def has_paginated_descendant(self) -> bool:
        for node in PreOrderIter(self):
            if node is not self and node.is_paginated:
                return True

        return False


class Document(Node):
    def __init__(self, definitions=None):
        self.definitions = definitions or []


class Definition(Node):
    pass


class FragmentDefinition(Definition):
    def __init__(self, name, type_condition, selections, directives=None):
        self.name = name
        self.type_condition = type_condition
        self.selections = selections
        self.directives = directives or []


class OperationDefinition(Definition):
    def __init__(self, selections, name=None, variable_definitions=None,
                 directives=None):
        self.selections = selections
        self.name = name
        self.variable_definitions = variable_definitions or []
        self.directives = directives or []


class Query(OperationDefinition):
    pass


class Mutation(OperationDefinition):
    pass


class Subscription(OperationDefinition):
    pass


class Selection(Node):
    pass


class Field(Selection):
    def __init__(self, name, alias=None, arguments=None, directives=None,
                 selections=None):
        self.name = name
        self.alias = alias
        self.arguments = arguments or []
        self.directives = directives or []
        self.selections = selections or []


class FragmentSpread(Selection):
    def __init__(self, name, directives=None):
        self.name = name
        self.directives = directives or []


class InlineFragment(Selection):
    def __init__(self, type_condition, selections, directives=None):
        self.type_condition = type_condition
        self.selections = selections
        self.directives = directives or []


class Argument(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Value(Node):
    def __init__(self, value):
        self.value = value


class VariableDefinition(Value):
    def __init__(self, name, type, default_value=None):
        self.name = name
        self.type = type
        self.default_value = default_value


class Variable(Value):
    def __init__(self, name):
        self.name = name


class Directive(Node):
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments or []


class Type(Node):
    pass


class NamedType(Type):
    def __init__(self, name):
        self.name = name


class ListType(Type):
    def __init__(self, type):
        self.type = type


class NonNullType(Type):
    def __init__(self, type):
        self.type = type


class TypeCondition(NamedType):
    pass
