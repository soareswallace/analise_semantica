from symboltable import *

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class BuildSymbolTableVisitor(NodeVisitor):
    def __init__(self, tree, scope_name, scope_level, enclosing_scope=None):
        self.ast = tree
        self.symbolTable = ScopedSymbolTable(scope_name, scope_level, enclosing_scope)
        self.scopes_inside = []

    def build(self):
        self.visit(self.ast)
        return self.symbolTable
    
    def BOOLEAN(self):
        return self.symbolTable.lookup('BOOLEAN')
    def INT(self):
        return self.symbolTable.lookup('INT')
    def STRING(self):
        return self.symbolTable.lookup('STRING')
    
    def erro(self, msg):
        raise Exception(msg)
    
    def visit_Program(self, node):
        for stm in node.stmts:
            self.visit(stm)
    
    def visit_VarDeclStm(self, node): 
        nome = node.id
        if self.symbolTable.lookup(nome) is None:
            tipo = self.symbolTable.lookup(node.type)
            simbolo = VarSymbol(nome, tipo)
            self.symbolTable.insert(nome, simbolo)
        else:
            self.erro("Identificador já declarado: '%s'" % nome)

    def visit_AssignStm(self, node): 
        nome_var = node.id 
        sym_var = self.symbolTable.lookup(nome_var)
        if sym_var is None:
            self.erro("Identificador não declarado: '%s'" % nome_var)
        else:
            tipo_var = sym_var.type
            tipo_exp = self.visit(node.exp)
            if tipo_var.name != tipo_exp.name: 
                self.erro('Variável espera por valor de tipo ' + str(tipo_var) + ', mas recebeu valor de tipo '+str(tipo_exp))

    def visit_InputStm(self, node): 
        if self.symbolTable.lookup(node.id) is None:
            self.erro("Identificador não declarado: '%s'" % node.id)
    
    def visit_PrintStm(self, node): 
        self.visit(node.exp)
    
    def visit_IfStm(self,node):
        tipo_condicao = self.visit(node.cond)
        if tipo_condicao == self.BOOLEAN():
            for stm in node.stmts:
                self.visit(stm)
        else: 
            self.erro('Condição do IF deve ser BOOLEAN, recebeu uma expressão de tipo '+str(tipo_condicao))
    
    def visit_WhileStm(self,node):
        tipo_condicao = self.visit(node.cond)
        if tipo_condicao == self.BOOLEAN():
            for stm in node.stmts:
                self.visit(stm)
        else: 
            self.erro('Condição do IF deve ser BOOLEAN, recebeu uma expressão de tipo '+str(tipo_condicao))

    def visit_BlockStm(self, node):
        if self.ast != node:
            newSymbolTable = BuildSymbolTableVisitor(node, "Block", self.symbolTable.scope_level + 1, self).build()
            self.scopes_inside.append(newSymbolTable)
        else:
            for stm in node.stmts:
                    self.visit(stm)

    def visit_TrueExpr(self, node):
        return self.BOOLEAN()
    def visit_FalseExpr(self, node):
        return self.BOOLEAN()
    def visit_NumExpr(self, node): 
        return self.INT()
    def visit_StringExpr(self, node): 
        return self.STRING()

    def visit_visit_UnaryPlusExpr(self, node): 
        return self.visit(node.exp)
    def visit_visit_UnaryMinusExpr(self, node): 
        return self.visit(node.exp)

    def visit_IdExpr(self, node): 
        sym = self.symbolTable.lookup(node.id)
        if sym is None:
            self.erro("Identificador não declarado: '%s'" % node.id)
        else:
            return sym.type

    def visit_SumExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == self.INT() and right_type == self.INT():
            return self.INT()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_SubExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == self.INT() and right_type == self.INT():
            return self.INT()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_MulExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == self.INT() and right_type == self.INT():
            return self.INT()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_DivExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == self.INT() and right_type == self.INT():
            return self.INT()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_NotExpr(self,node):
        self.visit(node.exp)

    def visit_EqualsExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == right_type :
            return self.BOOLEAN()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_NotEqualsExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == right_type :
            return self.BOOLEAN()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    #TODO ajustar depois para só permitir comparações de ordem em strings e inteiros
    def visit_GreaterThanEqualsExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == right_type :
            return self.BOOLEAN()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_GreaterThanExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == right_type :
            return self.BOOLEAN()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_LessThanEqualsExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == right_type :
            return self.BOOLEAN()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

    def visit_LessThanExpr(self,node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == right_type :
            return self.BOOLEAN()
        else: 
            self.erro('Tipos incompatíveis: ' + str(left_type) + ' e ' + str(right_type))

class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.ast = tree
        self.symbolTable = BuildSymbolTableVisitor(tree).build()
    
    def interpret(self):
        self.visit(self.ast)
    
    def erro(self, msg):
        raise Exception(msg)
    
    def visit_Program(self, node):
        for stm in node.stmts:
            self.visit(stm)
    
    def visit_VarDeclStm(self, node): 
        pass

    def visit_AssignStm(self, node): 
        nome = node.id 
        tipo = self.symbolTable.lookup(nome).type
        valor = self.visit(node.exp)
        symbol = VarSymbol(nome, tipo, valor)
        self.symbolTable.update(nome, symbol)

    def visit_InputStm(self, node): 
        nome = node.id 
        tipo = self.symbolTable.lookup(nome).type
        entrada_usuario = input()
        if tipo.name == 'INT': 
            valor = int(entrada_usuario)
        elif tipo.name == 'BOOLEAN': 
            true_values = ['True', 'true', 'T', 't']
            false_values = ['False', 'false', 'F', 'f']
            if entrada_usuario in true_values:
                valor = True
            elif entrada_usuario in false_values:
                valor = False
            else: 
                self.erro('Digite um valor booleano')
        else:
            valor = str(entrada_usuario)
        symbol = VarSymbol(nome, tipo, valor)
        self.symbolTable.update(nome, symbol)
    
    def visit_PrintStm(self, node): 
        print(self.visit(node.exp))
    
    def visit_IfStm(self,node):
        if self.visit(node.cond):
            for stm in node.stmts:
                self.visit(stm)
    
    def visit_WhileStm(self,node):
        while self.visit(node.cond):
            for stm in node.stmts:
                self.visit(stm)

    def visit_BlockStm(self,node):
        for stm in node.stmts:
            self.visit(stm)

    def visit_NumExpr(self, node): 
        return node.valor

    def visit_StringExpr(self, node): 
        return node.str

    def visit_IdExpr(self, node): 
        return self.symbolTable.lookup(node.id).value
    
    def visit_TrueExpr(self,node):
        return True
    def visit_FalseExpr(self,node):
        return False

    def visit_UnaryPlusExpr(self,node):
        return +(self.visit(node.exp))
    def visit_UnaryMinusExpr(self,node):
        return -(self.visit(node.exp))

    def visit_SumExpr(self,node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_SubExpr(self,node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_MulExpr(self,node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_DivExpr(self,node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_NotExpr(self,node):
        return not(self.visit(node.exp))

    def visit_EqualsExpr(self,node):
        return self.visit(node.left) == self.visit(node.right)

    def visit_NotEqualsExpr(self,node):
        return self.visit(node.left) != self.visit(node.right)

    def visit_GreaterThanEqualsExpr(self,node):
        return self.visit(node.left) >= self.visit(node.right)

    def visit_GreaterThanExpr(self,node):
        return self.visit(node.left) > self.visit(node.right)

    def visit_LessThanEqualsExpr(self,node):
        return self.visit(node.left) <= self.visit(node.right)

    def visit_LessThanExpr(self,node):
        return self.visit(node.left) < self.visit(node.right)