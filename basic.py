from lexer import *
from parser import *
from astnodes import *
from visitor import *
import sys

def main(): 
    if len(sys.argv) != 2:
        sys.exit("Erro: Precisamos de um arquivo como argumento.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    parser = Parser(lexer)
    prog = parser.program()    
    
    symbolTable = BuildSymbolTableVisitor(prog).build()
    print(symbolTable)

    # interpreter = Interpreter(prog)
    # interpreter.interpret()
    # print(interpreter.symbolTable)

main()