# Estructura del fichero actual

## Archivos que NO requieren ser modificados manualmente
Este fichero contiene un script 'clean.js' que recibe el archivo 'matrix_csv.csv'para devolver el mismo archivo pero limpio llamado '/output/matrix_csv.txt'.

Para realizar el proceso de limpieza ejecutar en el bash:
`$ node clean.js`

## Archivos que SI requieren ser modificados manualmete
Hay otro archivo llamado 'matrix_xls.xlsx' que contiene la matriz de transición para que el Usuario lo modifique según el diseño del AFND

## Como lo uso
1. Modifica el archivo ´matrix_xls.xlsx´ según tu necesidad
2. Transforma el archivo anterior a formato CSV con alguna herramient externa _Herramientas Sugeridas abajo v_
3. Coloca el archivo transformado en el directorio `/input` con siguiente nombre: `matrix_csv.csv`__.gitignore__
4. Ejecuta el siguiente comando: `$ node clean.js`
5. Se genera un archivo en el directorio `/output` listo para ser usado por el analizador léxico en python
6. Solo agrega un espacio después del último '_' de la primer fila
, si no el programa tronará
## Conversores XLSX -> CSV
https://www.zamzar.com/es/convert/xlsx-to-csv/  :)
https://convertio.co/es/xlsx-csv/               :(

