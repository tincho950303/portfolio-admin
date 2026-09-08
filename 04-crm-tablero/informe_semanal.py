from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
cli = pd.read_csv(BASE / ".." / "datasets" / "clientes.csv", dtype=str, encoding="utf-8-sig")
fac = pd.read_csv(BASE / ".." / "datasets" / "facturas.csv", dtype=str, encoding="utf-8-sig")

print(f"clientes: {len(cli)} facturas: {len(fac)}")
print("cond IVA:", cli["cond_iva"].value_counts().to_dict())
print("estados fac:", fac["estado"].value_counts().to_dict())
print(cli[["nombre","cond_iva","localidad"]].head(3).to_string())

def limpiar_importe(v):
    if pd.isna(v):
        return None
    s = str(v).strip().replace("$", "").strip()
    if s == "" or s.upper() == "MAL":
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    s = s.replace(" ", "")
    try:
        return round(float(s), 2)
    except ValueError:
        return None

def limpiar_fecha(v):
    if pd.isna(v):
        return None
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d-%m-%y", "%d/%m/%y"):
        try:
            return pd.to_datetime(s, format=fmt).date()
        except ValueError:
            continue
    try:
        return pd.to_datetime(s, dayfirst=True, errors="raise").date()
    except Exception:
        return None

from datetime import date
HOY = date(2026, 9, 4)
fac["total_limpio"] = fac["total"].apply(limpiar_importe)
fac["vto"] = fac["fecha_vto"].apply(limpiar_fecha)

# solo lo no cobrado cuenta como deuda
deuda = fac[fac["estado"].isin(["vencida", "pendiente"])].copy()
top = deuda.groupby(["cliente", "cuit"], as_index=False)["total_limpio"].sum()
top = top.rename(columns={"total_limpio": "deuda"}).sort_values("deuda", ascending=False)

prox = fac[(fac["estado"] == "pendiente") & (fac["vto"] >= HOY)].copy().sort_values("vto")

print(f"clientes con deuda: {len(top)} deuda total: {top['deuda'].sum():.2f}")
print(top.head(5).to_string())
print(f"próximos vtos pendientes: {len(prox)}")
print(prox[["nro_factura","cliente","vto","total_limpio"]].head(5).to_string())

OUT = BASE / "output"
OUT.mkdir(parents=True, exist_ok=True)
resumen = pd.DataFrame({
    "kpi": ["clientes_totales", "clientes_con_deuda", "deuda_total_ARS", "facturas_vencidas", "proximos_vtos_7d"],
    "valor": [len(cli), len(top), round(float(top["deuda"].sum()), 2), int((fac["estado"]=="vencida").sum()), len(prox)]
})

with pd.ExcelWriter(OUT / "informe_ejecutivo.xlsx", engine="openpyxl") as w:
    resumen.to_excel(w, sheet_name="resumen", index=False)
    top.to_excel(w, sheet_name="top_deudores", index=False)
    prox[["nro_factura","cliente","cuit","vto","total_limpio","cond_iva"]].to_excel(w, sheet_name="proximos_vtos", index=False)

print("OK informe_ejecutivo.xlsx")