from pathlib import Path
import pandas as pd
import re

BASE = Path(__file__).parent
INPUT = BASE / "input" / "ventas_sucias.csv"

def limpiar_cuit(valor):
    if pd.isna(valor):
        return ""
    digitos = re.sub(r"\D", "", str(valor))
    return digitos
def limpiar_fecha(valor):
    if pd.isna(valor):
        return None
    s = str(valor).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d-%m-%y", "%d/%m/%y"):
        try:
            return pd.to_datetime(s, format=fmt).date()
        except ValueError:
            continue
    try:
        return pd.to_datetime(s, dayfirst=True, errors="raise").date()
    except Exception:
        return None
def limpiar_importe(valor):
    if pd.isna(valor):
        return None
    s = str(valor).strip().replace("$", "").strip()
    if s == "" or s.upper() == "MAL":
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    s = s.replace(" ", "")
    try:
        return round(float(s), 2)
    except ValueError:
        return None
def limpiar_cantidad(valor):
    if pd.isna(valor):
        return None
    s = str(valor).strip().lower().replace("u", "").strip()
    if s == "":
        return None
    try:
        n = int(float(s))
        return n if n > 0 else None
    except ValueError:
        return None
def limpiar_texto(valor):
    if pd.isna(valor):
        return ""
    s = re.sub(r"\s+", " ", str(valor).strip())
    return s.title()
def motivo(row):
    fallas = []
    if len(str(row["cuit_limpio"])) != 11:
        fallas.append("CUIT inválido")
    if pd.isna(row["fecha_limpia"]):
        fallas.append("fecha inválida")
    if pd.isna(row["cantidad_limpia"]):
        fallas.append("cantidad inválida")
    if pd.isna(row["precio_limpio"]):
        fallas.append("precio inválido")
    if pd.isna(row["total_limpio"]):
        fallas.append("total inválido")
    if str(row.get("codigo_producto", "")).strip() == "":
        fallas.append("código vacío")
    return "; ".join(fallas)


df = pd.read_csv(INPUT, dtype=str, encoding="utf-8-sig")
# print(f"filas: {len(df)}")
# print(list(df.columns))
# print(df.head(3).to_string())

df["cuit_limpio"] = df["cuit"].apply(limpiar_cuit)
print(df[["cuit", "cuit_limpio"]].head(5).to_string())
print("CUIT con 11 digitos:", (df["cuit_limpio"].str.len() == 11).sum(), "de", len(df))

df["fecha_limpia"] = df["fecha"].apply(limpiar_fecha)
print(df[["fecha", "fecha_limpia"]].head(8).to_string())
print("fechas invalidas:", df["fecha_limpia"].isna().sum())

df["precio_limpio"] = df["precio_unit"].apply(limpiar_importe)
df["total_limpio"] = df["total"].apply(limpiar_importe)
print(df[["precio_unit", "precio_limpio", "total", "total_limpio"]].head(10).to_string())
print("precios invalidos:", df["precio_limpio"].isna().sum())

df["cantidad_limpia"] = df["cantidad"].apply(limpiar_cantidad)
df["cliente_limpio"] = df["cliente"].apply(limpiar_texto)
print("cantidades invalidas:", df["cantidad_limpia"].isna().sum())
print(df[["cantidad","cantidad_limpia","cliente","cliente_limpio"]].head(8).to_string())


df["motivo_error"] = df.apply(motivo, axis=1)
malos = df[df["motivo_error"] != ""].copy()
buenos = df[df["motivo_error"] == ""].copy()
print(f"malos: {len(malos)} buenos: {len(buenos)}")

antes = len(buenos)
buenos = buenos.drop_duplicates(subset=["id_venta", "codigo_producto", "cantidad_limpia", "total_limpio"], keep="first")
print(f"duplicados: {antes - len(buenos)} limpias final: {len(buenos)}")


