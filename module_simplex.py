import numpy as np
from tabulate import tabulate  # Importar tabulate para formatear la tabla

class SimplexTable:
    def __init__(self, c, A, b):
        self.c = np.array(c)  # Coeficientes de la función objetivo
        self.A = np.array(A)  # Coeficientes de las restricciones
        self.b = np.array(b)  # Lado derecho de las restricciones
        self.num_vars = len(c)
        self.num_constraints = len(b)
        self.table = self.initialize_table()

    def initialize_table(self):
        # Crear la tabla simplex inicial
        table = np.zeros((self.num_constraints + 1, self.num_vars + self.num_constraints + 1))
        
        # Llenar la tabla con los coeficientes de las restricciones
        table[:-1, :self.num_vars] = self.A
        table[:-1, self.num_vars:self.num_vars + self.num_constraints] = np.eye(self.num_constraints)
        table[:-1, -1] = self.b
        
        # Llenar la última fila con los coeficientes de la función objetivo
        table[-1, :self.num_vars] = -self.c
        
        return table

    def pivot(self, row, col):
        # Realizar el pivoteo en la tabla simplex
        pivot_value = self.table[row, col]
        self.table[row, :] /= pivot_value
        for r in range(self.table.shape[0]):
            if r != row:
                self.table[r, :] -= self.table[r, col] * self.table[row, :]

    def solve(self):
        # Aplicar el método simplex
        while np.any(self.table[-1, :-1] < 0):
            # Encontrar la columna pivote (la más negativa en la última fila)
            col = np.argmin(self.table[-1, :-1])
            
            # Encontrar la fila pivote (la mínima razón positiva)
            ratios = self.table[:-1, -1] / self.table[:-1, col]
            row = np.argmin(ratios[ratios > 0])
            
            # Realizar el pivoteo
            self.pivot(row, col)
        
        return self.table

    def get_final_table(self):
        # Obtener la tabla final después de aplicar el método simplex
        return self.table

    def format_table(self):
        # Formatear la tabla para una mejor visualización
        headers = [f"x{i+1}" for i in range(self.num_vars)] + [f"s{i+1}" for i in range(self.num_constraints)] + ["b"]
        table_data = self.table.tolist()
        return tabulate(table_data, headers=headers, floatfmt=".2f", tablefmt="grid")

    def __str__(self):
        # Representación en cadena de la tabla formateada
        return self.format_table()