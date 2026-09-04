# generar_datasets.py - Día 1 portfolio-admin
# Solo stdlib. Genera datos SIMULADOS argentinos.
# Uso: python generar_datasets.py
import csv
import random
from pathlib import Path
from datetime import date, timedelta

random.seed(42)
BASE = Path(__file__).parent

HOY = date(2026, 9, 4)
INICIO = date(2026, 6, 1)

def rand_fecha():
    delta = (HOY - INICIO).days
    return INICIO + timedelta(days=random.randint(0, delta))

def fmt_arg(importe: float) -> str:
    # "$ 12.345,67" estilo sucio argentino
    entero = int(importe)
    dec = int(round((importe - entero) * 100))
    s = f"{entero:,}".replace(",", ".")
    return f"$ {s},{dec:02d}"

def gen_cuit(pref=None):
    pref = pref or random.choice(["20", "27", "30"])
    medio = "".join(str(random.randint(0, 9)) for _ in range(8))
    ver = str(random.randint(0, 9))
    return f"{pref}{medio}{ver}"  # 11 dígitos sin guiones

CATEGORIAS = {
    "Librería": ["Resma A4 75g", "Lapicera azul x12", "Carpeta oficio", "Cuaderno espiral", "Tóner alternativo"],
    "Limpieza": ["Lavandina 5L", "Detergente 5L", "Papel higiénico x30", "Desinfectante 5L", "Bolsa consorcio x100"],
    "Oficina": ["Silla ergonómica", "Escritorio 120cm", "Cinta embalaje x6", "Caja archivo", "Calculadora"],
    "Electrónica": ["Mouse USB", "Teclado USB", "Alargue 5m", "Auricular vincha", "Webcam HD"],
    "Almacén": ["Yerba 1kg", "Azúcar 1kg", "Café molido 500g", "Galletita surtida", "Agua 20L"],
}
PROVEEDORES = ["Distribuidora Sur SA", "Mayorista CABA SRL", "Limpieza Total SA", "Oficina Ya SRL", "Electro GBA SA"]
VENDEDORES = ["Lucía Gómez", "Martín Pérez", "Camila Ruiz", "Diego Torres"]
MEDIOS = ["Efectivo", "Transferencia", "Mercado Pago", "Tarjeta"]
LOCALIDADES = ["CABA", "Lanús", "Quilmes", "Morón", "La Plata", "Córdoba", "Rosario"]
APELLIDOS = ["García", "Fernández", "González", "Pérez", "Rodríguez", "López", "Martínez", "Sánchez", "Romero", "Díaz"]
NOMBRES = ["Juan", "María", "Carlos", "Lucía", "Pedro", "Ana", "Martín", "Camila", "Diego", "Sofía"]
EMPRESAS = ["Kiosco El Faro", "Librería Central", "Oficina Norte SRL", "Comercio San Martín", "Almacén Don Pepe", "Tech Hogar SA"]

# 1. productos.csv (50)
productos = []
sku = 1000
for cat, items in CATEGORIAS.items():
    for base in items:
        for var in (["", " Plus", " Eco"] if len(productos) < 45 else [""]):
            if len(productos) >= 50:
                break
            sku += 1
            compra = round(random.uniform(1500, 40000), 2)
            venta = round(compra * random.uniform(1.3, 1.8), 2)
            stock = random.randint(0, 200)
            minimo = random.choice([10, 15, 20, 30])
            productos.append([f"SKU-{sku}", f"{base}{var}", cat, random.choice(PROVEEDORES), compra, venta, stock, minimo])
            if len(productos) >= 50:
                break

with open(BASE / "productos.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["codigo", "nombre", "categoria", "proveedor", "precio_compra", "precio_venta", "stock_actual", "stock_minimo"])
    w.writerows(productos)

# 2. clientes.csv (40)
clientes = []
for i in range(40):
    if i < 15:
        nombre = random.choice(EMPRESAS) + f" {i+1}"
        cond = random.choice(["Responsable Inscripto", "Monotributo"])
        pref = "30" if "SRL" in nombre or "SA" in nombre else random.choice(["20", "27", "30"])
    elif i < 30:
        nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
        cond = random.choice(["Monotributo", "Consumidor Final"])
        pref = random.choice(["20", "27"])
    else:
        nombre = "Consumidor Final"
        cond = "Consumidor Final"
        pref = "20"
    cuit = gen_cuit(pref)
    email = f"cliente{i+1}@ejemplo.com.ar"
    tel = f"11-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    loc = random.choice(LOCALIDADES)
    clientes.append([i+1, nombre, cuit, cond, email, tel, loc])

with open(BASE / "clientes.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id_cliente", "nombre", "cuit", "cond_iva", "email", "telefono", "localidad"])
    w.writerows(clientes)

# 3. ventas_limpias.csv (200)
ventas = []
for i in range(1, 201):
    prod = random.choice(productos)
    cli = random.choice(clientes)
    fecha = rand_fecha()
    cant = random.randint(1, 20)
    precio = prod[5]
    total = round(cant * precio, 2)
    ventas.append([i, fecha.isoformat(), cli[1], cli[2], prod[0], prod[1], cant, precio, total, random.choice(MEDIOS), random.choice(VENDEDORES)])

with open(BASE / "ventas_limpias.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id_venta", "fecha", "cliente", "cuit", "codigo_producto", "producto", "cantidad", "precio_unit", "total", "medio_pago", "vendedor"])
    w.writerows(ventas)

# 4. ventas_sucias.csv (misma + suciedad para P2)
sucias = []
for row in ventas:
    r = list(row)
    # r index: 0 id,1 fecha,2 cliente,3 cuit,4 cod,5 prod,6 cant,7 precio,8 total,9 medio,10 vend
    if random.random() < 0.12:
        # fecha a DD/MM/AAAA o DD-MM-YY
        y, m, d = r[1].split("-")
        r[1] = f"{d}/{m}/{y}" if random.random() < 0.5 else f"{d}-{m}-{y[2:]}"
    if random.random() < 0.15:
        r[8] = fmt_arg(float(r[8]))
        r[7] = fmt_arg(float(r[7]))
    if random.random() < 0.12:
        c = r[3]
        r[3] = f"{c[:2]}-{c[2:10]}-{c[10:]}" if random.random() < 0.5 else f" {c} "
    if random.random() < 0.06:
        r[2] = "  " + r[2].upper().replace("  ", " ") + "  " if random.random() < 0.5 else r[2].lower()
    if random.random() < 0.03:
        r[6] = "" if random.random() < 0.5 else f"{r[6]}u"
    sucias.append(r)

# duplicados 5%
for _ in range(10):
    sucias.append(random.choice(sucias))
# filas rotas
for _ in range(8):
    sucias.append(["", "99/99/9999", "DATO ROTO", "123", "", "", "", "", "$ MAL", "", ""])

random.shuffle(sucias)
with open(BASE / "ventas_sucias.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id_venta", "fecha", "cliente", "cuit", "codigo_producto", "producto", "cantidad", "precio_unit", "total", "medio_pago", "vendedor"])
    w.writerows(sucias)

# 5. facturas.csv (100) + pagos + extracto
facturas = []
for n in range(1, 101):
    cli = random.choice(clientes)
    cond = cli[3]
    tipo = "A" if cond == "Responsable Inscripto" else (random.choice(["B", "C"]) if cond == "Monotributo" else "B")
    emision = rand_fecha()
    vto = emision + timedelta(days=random.choice([15, 30]))
    neto = round(random.uniform(20000, 500000), 2)
    iva = round(neto * 0.21, 2) if tipo in ("A", "B") else 0.0
    total = round(neto + iva, 2)
    estado = random.choices(["pagada", "pendiente", "vencida"], weights=[55, 25, 20])[0]
    if vto >= HOY and estado == "vencida":
        estado = "pendiente"
    if vto < HOY and estado == "pendiente":
        estado = "vencida"
    cae = "".join(str(random.randint(0, 9)) for _ in range(14))
    facturas.append([f"0001-{n:08d}", tipo, emision.isoformat(), vto.isoformat(), cli[1], cli[2], cond, neto, iva, total, estado, cae])

with open(BASE / "facturas.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["nro_factura", "tipo", "fecha_emision", "fecha_vto", "cliente", "cuit", "cond_iva", "neto", "iva21", "total", "estado", "cae_simulado"])
    w.writerows(facturas)

# pagos: 70% de las pagadas + algunas parciales
pagos = []
pid = 1
for fac in facturas:
    if fac[10] == "pagada" and random.random() < 0.9:
        emi = date.fromisoformat(fac[2])
        fpago = emi + timedelta(days=random.randint(0, 30))
        pagos.append([pid, fac[0], fpago.isoformat(), fac[9], random.choice(["Transferencia", "Mercado Pago", "Efectivo"])])
        pid += 1
    elif fac[10] == "pendiente" and random.random() < 0.1:
        pagos.append([pid, fac[0], HOY.isoformat(), fac[9], "Transferencia"])
        pid += 1

with open(BASE / "pagos.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id_pago", "nro_factura", "fecha_pago", "importe", "medio"])
    w.writerows(pagos)

# extracto: casi todos los pagos +/- 2 días y +/- diferencia, + 5 movimientos extra
extracto = []
eid = 1
for p in pagos:
    if random.random() < 0.92:
        fp = date.fromisoformat(p[2]) + timedelta(days=random.choice([-1, 0, 0, 1, 2]))
        imp = p[3]
        if random.random() < 0.08:
            imp = round(imp + random.choice([-100, 100, -500]), 2)  # diferencia para detectar
        extracto.append([eid, fp.isoformat(), f"TRANSF {p[1]}", imp])
        eid += 1
for _ in range(5):
    extracto.append([eid, rand_fecha().isoformat(), "ACREDITACIÓN VARIOS / COMISIÓN", round(random.uniform(5000, 80000), 2)])
    eid += 1

with open(BASE / "extracto_bancario.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id_extracto", "fecha", "descripcion", "importe"])
    w.writerows(extracto)

print(f"OK datasets en {BASE}")
print(f"productos={len(productos)} clientes={len(clientes)} ventas_limpias={len(ventas)} ventas_sucias={len(sucias)} facturas={len(facturas)} pagos={len(pagos)} extracto={len(extracto)}")
