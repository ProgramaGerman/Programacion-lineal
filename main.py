import sys
import numpy as np
from scipy.optimize import linprog
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox

class LinearProgrammingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Programación Lineal con PyQt6")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.funcion_objetivo_label = QLabel("Función Objetivo (coeficientes separados por comas):")
        self.layout.addWidget(self.funcion_objetivo_label)

        self.funcion_objetivo_input = QLineEdit()
        self.layout.addWidget(self.funcion_objetivo_input)

        self.restricciones_label = QLabel("Restricciones (una por línea, coeficientes separados por comas, seguidos de <=, >=, o = y el valor):")
        self.layout.addWidget(self.restricciones_label)

        self.restricciones_input = QTextEdit()
        self.layout.addWidget(self.restricciones_input)

        self.calcular_button = QPushButton("Calcular")
        self.calcular_button.clicked.connect(self.calcular)
        self.layout.addWidget(self.calcular_button)

        self.resultado_label = QLabel("Resultado:")
        self.layout.addWidget(self.resultado_label)

        self.resultado_output = QTextEdit()
        self.resultado_output.setReadOnly(True)
        self.layout.addWidget(self.resultado_output)

        self.central_widget.setLayout(self.layout)

    def calcular(self):
        try:
            # Obtener y validar la función objetivo
            funcion_objetivo = self.funcion_objetivo_input.text().strip()
            if not funcion_objetivo:
                raise ValueError("La función objetivo no puede estar vacía.")
            c = [float(int(coef.strip())) for coef in funcion_objetivo.split(",")]

            # Obtener y validar las restricciones
            restricciones = self.restricciones_input.toPlainText().strip().split('\n')
            if not restricciones:
                raise ValueError("Debe ingresar al menos una restricción.")

            A = []
            b = []
            for restriccion in restricciones:
                if not restriccion.strip():
                    continue  # Ignorar líneas vacías
                partes = restriccion.split()
                if len(partes) < 3:
                    raise ValueError(f"Formato incorrecto en la restricción: {restriccion}")
                
                # Obtener coeficientes
                coeficientes = [float(coef.strip()) for coef in partes[0].split(",")]
                A.append(coeficientes)

                # Obtener el valor del lado derecho
                b.append(float(partes[-1]))

            # Resolver el problema de programación lineal
            res = linprog(c, A_ub=A, b_ub=b, method='simplex')

            # Mostrar los resultados
            self.resultado_output.clear()
            self.resultado_output.append(f"Valor óptimo: {res.fun}")
            self.resultado_output.append(f"Solución: {res.x}")
            self.resultado_output.append("\nTabla final:")
            self.resultado_output.append(str(res))
            self.resultado_output.append("\nPrecios sombra:")
            self.resultado_output.append(str(res.slack))

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error en los datos de entrada: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinearProgrammingApp()
    window.show()
    sys.exit(app.exec())