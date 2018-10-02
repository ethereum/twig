from twig.utils.compiler import generate_contract_types, generate_inline_sources


class Compiler:
    def __init__(self, sources, backend):
        self.sources = sources
        self.backend = backend
        self.output = None

    def compile(self):
        self.output = self.backend.compile(self.sources)

    def get_contract_types(self):
        if not self.output:
            self.compile()
        return generate_contract_types(self.output)

    def get_source_tree(self):
        if not self.output:
            self.compile()
        return generate_inline_sources(self.output)
