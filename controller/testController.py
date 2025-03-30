from controller.controller import TreasuryController
from model.model import TreasuryModel
import pandas as pd
import os


def test_treasury():
    # Eliminar archivo previo si existe para un test limpio
    test_file = "treasury_record.csv"
    if os.path.exists(test_file):
        os.remove(test_file)

    controller = TreasuryController()

    # Agregar datos de prueba
    controller.add_new_data("2025-03-01", "2025-03-05", "Empresa A", "Pago servicio", 1000, "I")
    controller.add_new_data("2025-03-02", "2025-03-06", "Empresa B", "Compra materiales", 4500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa A", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa B", "Compra materiales", 2500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa D", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-08", "2025-03-09", "Empresa C", "Compra materiales", 3500, "E")
    controller.add_new_data("2025-03-01", "2025-03-05", "Empresa A", "Pago servicio", 1000, "I")
    controller.add_new_data("2025-03-02", "2025-03-06", "Empresa B", "Compra materiales", 500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa A", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa F", "Compra materiales", 2500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa D", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-08", "2025-03-09", "Empresa C", "Compra materiales", 3500, "E")
    controller.add_new_data("2025-03-01", "2025-03-05", "Empresa A", "Pago servicio", 1000, "I")
    controller.add_new_data("2025-03-02", "2025-03-06", "Empresa E", "Compra materiales", 500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa A", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa B", "Compra materiales", 2500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa E", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-08", "2025-03-09", "Empresa C", "Compra materiales", 3500, "E")
    controller.add_new_data("2025-03-08", "2025-03-09", "Empresa C", "Compra materiales", 3500, "E")
    controller.add_new_data("2025-03-01", "2025-03-05", "Empresa A", "Pago servicio", 1000, "I")
    controller.add_new_data("2025-03-02", "2025-03-06", "Empresa B", "Compra materiales", 500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa A", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa F", "Compra materiales", 2500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa D", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-08", "2025-03-09", "Empresa C", "Compra materiales", 3500, "E")
    controller.add_new_data("2025-03-01", "2025-03-05", "Empresa A", "Pago servicio", 1000, "I")
    controller.add_new_data("2025-03-02", "2025-03-06", "Empresa E", "Compra materiales", 500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa A", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa B", "Compra materiales", 2500, "E")
    controller.add_new_data("2025-03-06", "2025-03-09", "Empresa E", "Pago servicio", 2000, "I")
    controller.add_new_data("2025-03-08", "2025-03-09", "Empresa C", "Compra materiales", 5500, "E")


    # Obtener todos los datos
    data = controller.get_data()
    print("\n--- Registros ---")
    print(data)

    # Obtener resumen de ingresos
    income_total, income_avg = controller.get_income_summary()
    print("\n--- Resumen de Ingresos ---")
    print(f"Total: {income_total}, Promedio: {income_avg}")

    # Obtener resumen de gastos
    expense_total, expense_avg = controller.get_expenses_summary()
    print("\n--- Resumen de Gastos ---")
    print(f"Total: {expense_total}, Promedio: {expense_avg}")

    # Obtener datos agrupados por empresa
    print("\n--- Datos por Empresa (Ingresos) ---")
    print(controller.get_data_by_company("I"))

    print("\n--- Datos por Empresa (Gastos) ---")
    print(controller.get_data_by_company("E"))

    # Obtener balance mensual
    print("\n--- Balance Mensual ---")
    print(controller.get_monthly_balance())


if __name__ == "__main__":
    test_treasury()