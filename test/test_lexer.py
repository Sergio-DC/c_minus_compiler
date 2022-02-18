import code
import unittest

from Parser import parser, setSourceCode
from semantica import getTestOutput, semantica
from cgen import codeGen
#import pdb; pdb.set_trace()


class TestSemantics(unittest.TestCase):
    def test_code_with_errors_1(self):
        f = open('./test_cases/semantics/test_1.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)

        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        actualList = getTestOutput()
        expectedList = ['Error variable no declarada 2', 'Error missing return statement']
        self.assertTrue(actualList)
        for index, actual in enumerate(actualList, start=0):
            self.assertEqual(expectedList[index], actual)
        actualList.clear()
        expectedList.clear()
        #self.assertEquals(5, 5)

        ##semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        ##codeGen(AST, "salida.asm")

    def test_code_with_errors_2(self):
        f = open('./test_cases/semantics/test_2.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)

        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        actualList = getTestOutput()
        expectedList = ['Error el tipo debe ser INT']
        self.assertTrue(actualList)
        for index, actual in enumerate(actualList, start=0):
                    self.assertEqual(expectedList[index], actual)
        actualList.clear()
        expectedList.clear()
        