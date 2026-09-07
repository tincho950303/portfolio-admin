from limpiar_reporte import *
OUTPUT_DIR = BASE / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

limpio = buenos[buenos["motivo_error"] == ""].copy()  # ya lo tienes como buenos sin dup
# ordena columnas lindas para el jefe
limpio_final = pd.DataFrame({
    "id_venta": buenos["id_venta"],
    "fecha": buenos["fecha_limpia"],
    "cliente": buenos["cliente_limpio"],
    "cuit": buenos["cuit_limpio"],
    "codigo_producto": buenos["codigo_producto"],
    "cantidad": buenos["cantidad_limpia"],
    "precio_unit": buenos["precio_limpio"],
    "total": buenos["total_limpio"],
    "medio_pago": buenos["medio_pago"],
    "vendedor": buenos["vendedor"],
}).sort_values("fecha")

with pd.ExcelWriter(OUTPUT_DIR / "reporte_limpio.xlsx", engine="openpyxl") as w:
    limpio_final.to_excel(w, sheet_name="limpio", index=False)
    malos.to_excel(w, sheet_name="errores", index=False)
    pd.DataFrame({"métrica": ["leídas","limpias","errores","duplicados"], "valor": [len(df), len(buenos), len(malos), 10]}).to_excel(w, sheet_name="resumen", index=False)

print("OK excel generado")