Problema:
Maximizar la función objetivo:
Z = 3x1 + 5x2
 

Sujeto a las restricciones:
1,0 <= 4
0,2 <= 12
3,2 <= 18
Paso 1: Convertir el problema a la forma estándar
El programa resuelve problemas de minimización, por lo que debemos convertir la función objetivo de maximización a minimización multiplicando por -1:

Z - 3x1 - 5x2
 

Las restricciones ya están en la forma estándar (desigualdades de tipo <=).

Paso 2: Ingresar los datos en el programa
Función objetivo:

Ingresar los coeficientes de la función objetivo separados por comas:

3, 5

Restricciones:

Ingresar cada restricción en una línea, con los coeficientes separados por comas, seguidos de <= y el valor del lado derecho:


1, 0 <= 4
0, 2 <= 12
3, 2 <= 18


Paso 3: Ejecutar el programa
Al ejecutar el programa, aparecerá una ventana con los campos para ingresar la función objetivo y las restricciones.

Ingresa los datos como se describió anteriormente.

Haz clic en el botón Calcular.

Paso 4: Resultados
El programa mostrará los siguientes resultados en el área de texto:


Valor óptimo: -36.0
Solución: [2. 6.]

Tabla final:
     con: array([], dtype=float64)
     fun: -36.0
 message: 'Optimization terminated successfully.'
     nit: 3
   slack: array([2., 0., 0.])
  status: 0
 success: True
       x: array([2., 6.])

Precios sombra:
[2. 0. 0.]
Explicación de los resultados
Valor óptimo: El valor máximo de la función objetivo es 
Z = 36
Z=36 (el programa muestra -36 porque trabajamos con la minimización de −Z).

Solución: Los valores de 
x1 ​y x2
que maximizan la función objetivo son:


Tabla final: Muestra información detallada del resultado, como el número de iteraciones (nit), el estado del problema (status), y si la optimización fue exitosa (success).

Precios sombra (holguras): Indican cuánto "sobra" en cada restricción:

La primera restricción (
x1 ≤ 4
​
 ≤4) tiene una holgura de 2, lo que significa que 
x1 = 2

​
 =2 está 2 unidades por debajo del límite.

Las otras dos restricciones tienen holgura 0, lo que indica que son activas (es decir, se cumplen con igualdad).

Resumen
El programa resuelve el problema de programación lineal y muestra:

El valor óptimo de la función objetivo.

Los valores de las variables de decisión.

La tabla final del método simplex.

Las holguras de las restricciones (precios sombra).
