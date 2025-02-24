import sys
import pulp
import tkinter as tk
from tkinter import messagebox, scrolledtext

class LinearProgrammingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Programación Lineal con Tkinter y PuLP")
        self.root.geometry("600x400")

        self.layout = tk.Frame(self.root)
        self.layout.pack(padx=10, pady=10)

        self.funcion_objetivo_label = tk.Label(self.layout, text="Función Objetivo (coeficientes separados por comas):")
        self.funcion_objetivo_label.pack()

        self.funcion_objetivo_input = tk.Entry(self.layout, width=50)
        self.funcion_objetivo_input.pack()

        self.restricciones_label = tk.Label(self.layout, text="Restricciones (una por línea, coeficientes separados por comas, seguidos de <=, >=, o = y el valor):")
        self.restricciones_label.pack()

        self.restricciones_input = scrolledtext.ScrolledText(self.layout, width=50, height=10)
        self.restricciones_input.pack()

        self.calcular_button = tk.Button(self.layout, text="Calcular", command=self.calcular)
        self.calcular_button.pack(pady=10)

        self.resultado_label = tk.Label(self.layout, text="Resultado:")
        self.resultado_label.pack()

        self.resultado_output = scrolledtext.ScrolledText(self.layout, width=50, height=10)
        self.resultado_output.pack()

        self.mostrar_tabla_button = tk.Button(self.layout, text="Mostrar Tabla Final", command=self.mostrar_tabla, state=tk.DISABLED)
        self.mostrar_tabla_button.pack(pady=10)

        self.tabla_final = None  # Variable para almacenar la tabla final

    def calcular(self):
        try:
            # Obtener y validar la función objetivo
            funcion_objetivo = self.funcion_objetivo_input.get().strip()
            if not funcion_objetivo:
                raise ValueError("La función objetivo no puede estar vacía.")
            c = [float(coef.strip()) for coef in funcion_objetivo.split(",")]

            # Obtener y validar las restricciones
            restricciones = self.restricciones_input.get("1.0", tk.END).strip().split('\n')
            if not restricciones:
                raise ValueError("Debe ingresar al menos una restricción.")

            # Crear el problema de programación lineal
            prob = pulp.LpProblem("Problema_Lineal", pulp.LpMaximize)

            # Definir las variables de decisión
            x = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(len(c))]

            # Definir la función objetivo
            prob += pulp.lpSum([c[i] * x[i] for i in range(len(c))])

            # Definir las restricciones
            for restriccion in restricciones:
                if not restriccion.strip():
                    continue  # Ignorar líneas vacías
                partes = restriccion.split()
                if len(partes) < 3:
                    raise ValueError(f"Formato incorrecto en la restricción: {restriccion}")
                
                # Obtener coeficientes
                coeficientes = [float(coef.strip()) for coef in partes[0].split(",")]
                operador = partes[-2]
                valor = float(partes[-1])

                # Agregar la restricción al problema
                if operador == "<=":
                    prob += pulp.lpSum([coeficientes[i] * x[i] for i in range(len(coeficientes))]) <= valor
                elif operador == ">=":
                    prob += pulp.lpSum([coeficientes[i] * x[i] for i in range(len(coeficientes))]) >= valor
                elif operador == "=":
                    prob += pulp.lpSum([coeficientes[i] * x[i] for i in range(len(coeficientes))]) == valor
                else:
                    raise ValueError(f"Operador no válido en la restricción: {restriccion}")

            # Resolver el problema
            prob.solve()

            # Mostrar los resultados
            self.resultado_output.delete("1.0", tk.END)
            self.resultado_output.insert(tk.END, f"Estado: {pulp.LpStatus[prob.status]}\n")
            self.resultado_output.insert(tk.END, f"Valor óptimo: {pulp.value(prob.objective)}\n")
            self.resultado_output.insert(tk.END, "Solución:\n")
            for v in prob.variables():
                self.resultado_output.insert(tk.END, f"{v.name} = {v.varValue}\n")

            # Almacenar la tabla final (en este caso, el estado del problema)
            self.tabla_final = f"Estado: {pulp.LpStatus[prob.status]}\n"
            self.tabla_final += f"Valor óptimo: {pulp.value(prob.objective)}\n"
            self.tabla_final += "Variables:\n"
            for v in prob.variables():
                self.tabla_final += f"{v.name} = {v.varValue}\n"
            self.tabla_final += "Restricciones:\n"
            for name, constraint in prob.constraints.items():
                self.tabla_final += f"{name}: {constraint}\n"

            # Habilitar el botón para mostrar la tabla final
            self.mostrar_tabla_button.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos de entrada: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def mostrar_tabla(self):
        if self.tabla_final is None:
            messagebox.showwarning("Advertencia", "No hay una tabla final para mostrar.")
            return

        # Crear una nueva ventana modal para mostrar la tabla final
        tabla_window = tk.Toplevel(self.root)
        tabla_window.title("Tabla Final")
        tabla_window.geometry("500x400")

        # Agregar un widget de texto para mostrar la tabla
        tabla_text = scrolledtext.ScrolledText(tabla_window, width=60, height=20)
        tabla_text.pack(padx=10, pady=10)
        tabla_text.insert(tk.END, self.tabla_final)
        tabla_text.config(state=tk.DISABLED)  # Hacer el texto de solo lectura

        # Botón para cerrar la ventana
        cerrar_button = tk.Button(tabla_window, text="Cerrar", command=tabla_window.destroy)
        cerrar_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearProgrammingApp(root)
    root.mainloop()