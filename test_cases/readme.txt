Esta carpeta contiene una serie de pruebas en el lenguaje C-, para verificar
la calidad de los siguientes puntos del Analizador Semántico:

TEST_0: Resolucion de calculo entre numeros y literales con una variable
TEST_1: Resolucion de calculo entre numeros y literales con varias Variables
TEST_2: Se detecta error cuando una variable no ha sido declarada
TEST_3: Se detecta error cuando una variable se ha declarado 2 veces localmente X
TEST_4: Los parametros de una funcion se guardan en la TS y en el campo de 'params' de la funcion declarada (Solamente el tipo) X
TEST_5: Declaracion de variables dentro de una funcion X
TEST_6: Declaracion de variables globales X
TEST_7: Combinacion del TEST_5 Y TEST_6 X
TEST_8: Se permite declarar una variable con el mismo nombre siempre y cuando esten en distintos ámbitos, una globalmente y otra localmente X
TEST_9: Si el tipo de retorno de una funcion es int y no devuelve nada se arroja error
TEST_10: Si el tipo de retorno es void y se devuelve un valor INT, se arroja error
TEST_11: Si se quiere declarar una funcion sin parametros, la seccion de parametros debera tener void X
TEST_12: No se permite declarar parametros en las funciones con esta estructura: void foo(void x) X

Probando:
TEST_8-Suspender
TEST_3-ACTIVO