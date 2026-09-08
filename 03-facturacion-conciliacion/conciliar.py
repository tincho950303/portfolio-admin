from pathlib import Path
import pandas as pd
from datetime import date
HOY = date(2026, 9, 4)


BASE = Path(__file__).parent
fac = pd.read_csv(BASE / "input" / "facturas.csv", dtype=str, encoding="utf-8-sig")
pag = pd.read_csv(BASE / "input" / "pagos.csv", dtype=str, encoding="utf-8-sig")
ext = pd.read_csv(BASE / "input" / "extracto_bancario.csv", dtype=str, encoding="utf-8-sig")

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

# print(f"facturas: {len(fac)} pagos: {len(pag)} extracto: {len(ext)}")
# print("estados:", fac["estado"].value_counts().to_dict())
# print(fac[["nro_factura","tipo","total","estado"]].head(3).to_string())
# print(pag.head(2).to_string())
# print(ext.head(2).to_string())

pag["fecha_limpia"] = pag["fecha_pago"].apply(limpiar_fecha)
pag["importe_limpio"] = pag["importe"].apply(limpiar_importe)
ext["fecha_limpia"] = ext["fecha"].apply(limpiar_fecha)
ext["importe_limpio"] = ext["importe"].apply(limpiar_importe)
fac["total_limpio"] = fac["total"].apply(limpiar_importe)
fac["vto_limpio"] = fac["fecha_vto"].apply(limpiar_fecha)

# print("pagos nulos:", pag[["fecha_limpia","importe_limpio"]].isna().sum().to_dict())
# print("extracto nulos:", ext[["fecha_limpia","importe_limpio"]].isna().sum().to_dict())

from datetime import date
HOY = date(2026, 9, 4)

# 1. Concilia pagos -> extracto
usados = set()
filas = []
for _, p in pag.iterrows():
    match = None
    for _, e in ext.iterrows():
        if e["id_extracto"] in usados:
            continue
        if abs(p["importe_limpio"] - e["importe_limpio"]) > 1.0:
            continue
        dias = abs((p["fecha_limpia"] - e["fecha_limpia"]).days)
        if dias <= 2:
            match = e
            break
    if match is not None:
        usados.add(match["id_extracto"])
        filas.append({**p.to_dict(), "estado_conciliacion": "conciliado", "id_extracto": match["id_extracto"]})
    else:
        filas.append({**p.to_dict(), "estado_conciliacion": "faltante_en_extracto", "id_extracto": ""})

conc = pd.DataFrame(filas)
falt_sistema = ext[~ext["id_extracto"].isin(usados)].copy()
falt_sistema["estado_conciliacion"] = "faltante_en_sistema"

print(f"conciliados: {(conc['estado_conciliacion']=='conciliado').sum()} faltantes extracto: {(conc['estado_conciliacion']=='faltante_en_extracto').sum()} faltantes sistema: {len(falt_sistema)}")

# 2. Morosos: vencidas
morosos = fac[fac["estado"] == "vencida"].copy()
print(f"morosos: {len(morosos)} deuda total: {morosos['total_limpio'].sum():.2f}")

# 3. Excel
OUT = BASE / "output"
OUT.mkdir(parents=True, exist_ok=True)
with pd.ExcelWriter(OUT / "conciliacion.xlsx", engine="openpyxl") as w:
    conc.to_excel(w, sheet_name="pagos", index=False)
    falt_sistema.to_excel(w, sheet_name="faltantes_sistema", index=False)
    morosos.to_excel(w, sheet_name="morosos", index=False)
print("OK conciliacion.xlsx")