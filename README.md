# Laboratorio 7 - simplificación de gramáticas

### Alejandra Sierra 
### Camila Sandoval

El programa `simplificar_gramatica.py` valida un archivo de producciones y
elimina las producciones-epsilon mostrando el procedimiento completo. Usa
estructuras sencillas (`dict`, `list` y `set`) y nombres breves como
`prods`, `e`, `elim_e` y `prods_sin_e`.



## Ejecución

Desde esta carpeta:

```bash
python simplificar_gramatica.py gramatica1.txt
python simplificar_gramatica.py gramatica2.txt
```

Cada línea debe tener un no terminal mayúsculo, `->` y uno o más cuerpos
separados por `|`. Los cuerpos pueden contener letras, dígitos o ser exactamente
`ε`. Ejemplo válido:

```text
S -> 0A0 | 1B1 | BB
```

Si una línea es inválida, el programa muestra su número y termina con código 1.


## Criterio usado para epsilon

Se sigue el procedimiento de clase: se hallan todos los símbolos anulables y,
para cada cuerpo con `m` apariciones anulables, se recorren los `2^m` casos de
presencia/ausencia. No se vuelve a agregar el cuerpo vacío, de modo que
`L(G') = L(G) - {ε}`.
