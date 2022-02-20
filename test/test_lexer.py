import code
import unittest

from Parser import parser, setParserDebugMode, setSourceCode
from semantica import getTestOutput, semantica
from cgen import codeGen
#import pdb; pdb.set_trace()

class TestSemantics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._actualList = []
        cls._expectedList = []
        
        
    def test_code_with_errors_1(self):
        f = open('./test_cases/semantics/test_error_1.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)
        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        self._actualList = getTestOutput()
        self._expectedList = ['Error variable no declarada 2', 'Error missing return statement']
        self.assertTrue(self._actualList)
        for index, actual in enumerate(self._actualList, start=0):
            self.assertEqual(self._expectedList[index], actual)
        self._actualList.clear()
        self._expectedList.clear()
        

    def test_code_with_errors_2(self):
        f = open('./test_cases/semantics/test_error_2.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)

        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        self._actualList = getTestOutput()
        self._expectedList = ['Error el tipo debe ser INT']
        self.assertTrue(self._actualList)
        for index, actual in enumerate(self._actualList, start=0):
                    self.assertEqual(self._expectedList[index], actual)
        self._actualList.clear()
        self._expectedList.clear()

    #def test_code_with_errors_3(self):
    #    f = open('./test_cases/semantics/test_error_3.c-', 'r')
    #    sourceCode = f.read()
    #    f.close()
    #    setSourceCode(sourceCode)

    #    AST = parser()
    #    semantica(AST, False, True)#Revisar modos de impresion antes de enviar
    #    self._actualList = getTestOutput()
    #    self._expectedList = ['Error en la expresión de declaracion']
    #    self.assertTrue(self._actualList)
    #    for index, actual in enumerate(self._actualList, start=0):
    #                self.assertEqual(self._expectedList[index], actual)
    #    self._actualList.clear()
    #    self._expectedList.clear()
        
    def test_correct_code_1(self):
        f = open('./test_cases/semantics/test_correct_1.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)

        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        self._actualList = getTestOutput()
        self.assertFalse(self._actualList)

        self._actualList.clear()
        

    def test_correct_code_2(self):
        f = open('./test_cases/semantics/test_correct_2.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)

        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        self._actualList = getTestOutput()
        self.assertFalse(self._actualList)

        self._actualList.clear()
        
    def test_correct_code_3(self):
        f = open('./test_cases/semantics/test_correct_3.c-', 'r')
        sourceCode = f.read()
        f.close()
        setSourceCode(sourceCode)

        AST = parser()
        semantica(AST, False, True)#Revisar modos de impresion antes de enviar
        self._actualList = getTestOutput()
        self.assertFalse(self._actualList)

        self._actualList.clear()
        