# AGENT.md - portfolio-admin

> Guía operativa para agentes IA (y para el dueño) que trabajan en este repo.
> Objetivo: conseguir trabajo rápido como Auxiliar / Asistente Administrativo en Zonajobs / Computrabajo Argentina sin experiencia previa, demostrando con 4 proyectos verificables el manejo de Google Sheets + Python.

## 1. Contexto del proyecto

- **Perfil objetivo:** Asistente Administrativo | Sheets Avanzado + Python para automatización | Data Entry y Reportes.
- **Mercado:** Argentina, CABA/GBA e interior. Avisos tipo: auxiliar administrativo, data entry, back office, facturación, control stock, conciliación, CRM.
- **Stack permitido:** Python 3.10+ stdlib + `pandas` + `openpyxl` para reportes. Google Sheets (tablas dinámicas, XLOOKUP/BUSCARV, QUERY, validaciones, formato condicional). Nada de frameworks web, nada de datos reales.
- **Idioma:** todo en español rioplatense neutro. Fechas `DD/MM/AAAA`. Moneda `ARS $`. Archivos `UTF-8 con BOM` para abrir bien en Excel/Sheets Argentina.

## 2. Estructura del repo (no cambiar sin avisar)

```
portfolio-admin/
  AGENT.md
  README.md                # lo que lee el reclutador, 1 página, con links
  links.txt                # links públicos Drive + GitHub + video Loom
  datasets/                # datos base SIMULADOS, fuente de verdad
    productos.csv
    ventas_limpias.csv
    ventas_sucias.csv      # input intencionalmente sucio para P2
    facturas.csv
    pagos.csv
    extracto_bancario.csv
    clientes.csv
  01-stock-ventas-sheets/  # P1: solo Sheets + capturas + instructivo
  02-reporte-automatico-python/  # P2: input/ + limpiar_reporte.py + output/
    input/
    output/
  03-facturacion-conciliacion/   # P3: facturador + conciliador
    input/
    output/
  04-crm-tablero/          # P4: CRM + informe_ejecutivo
```

## 3. Reglas de negocio Argentina (obligatorias)

1. **CUIT:** 11 dígitos `20-XXXXXXXX-X`. Validar largo=11, solo números al limpiar. Aceptar con/sin guiones en input, normalizar sin guiones en output + columna `cuit_valido=true/false`.
2. **Condición IVA:** `Responsable Inscripto | Monotributo | Consumidor Final | Exento`. Factura A solo RI, B para resto, C para Monotributo.
3. **IVA 21%:** `neto * 0.21 = iva`, `total = neto + iva`. Redondeo 2 decimales.
4. **Medios de pago:** `Efectivo | Transferencia | Mercado Pago | Tarjeta`. Si es Transferencia/MP, exigir `CBU/Alias` simulado (nunca real).
5. **Importes:** input puede venir como `"$ 1.200,50"`, `"1200.50"`, `"1,200.50"`. Output siempre numérico `1200.50` + formato ARS en Excel.
6. **Fechas:** input mixto (`DD/MM/AAAA`, `AAAA-MM-DD`, `DD-MM-YY`). Output ISO `AAAA-MM-DD` en CSV + `DD/MM/AAAA` en Excel para lectura humana.
7. **Vencimientos:** factura `fecha_vto = fecha_emision + 15/30 días`. Estados: `pagada | pendiente | vencida` según hoy vs vto y pagos.
8. **Conciliación:** match `pagos vs extracto` por `abs(importe_pago - importe_extracto) < 1.0 AND abs(fecha_dif) <= 2 días`. Marcar `conciliado | faltante_en_extracto | faltante_en_sistema | diferencia_importe`.
9. **Nunca** usar nombres, CUIT, CBU, emails o teléfonos reales. Todo `SIMULADO`. Aclararlo en README y en cada Excel.

## 4. Convenciones de código y datos

- Scripts: un archivo por tarea, nombre `snake_case.py`, `if __name__ == "__main__":`, rutas relativas con `pathlib`, sin paths absolutos de Windows hardcodeados.
- Entrada desde `input/` o `../../datasets/`, salida siempre a `output/` (crear carpeta si no existe).
- Cada script imprime resumen por consola: filas leídas, filas limpias, errores, archivo generado. Y guarda `resumen.txt` en `output/`.
- Dependencias mínimas: preferir stdlib. Si se usa pandas/openpyxl, dejar `requirements.txt` con versiones y comando `pip install -r requirements.txt`.
- Excel de salida: primera fila freeze, autofiltro, anchos ajustados, pestaña `LEEME` de 5 líneas explicando el archivo para un jefe no técnico.
- CSV: `utf-8-sig`, separador `,`, header en minúsculas_snake_case.
- No borrar `datasets/`. Los proyectos copian, nunca modifican el original.

## 5. Workflow por día (plan 7 días, 2-3h/día)

- **Día 1 HECHO:** estructura + datasets. No avanzar a P2 sin datasets ok.
- **Día 2 P1:** armar Sheets desde `productos.csv` + `ventas_limpias.csv`. Entregable: link lectura + 2 capturas en `01-stock-ventas-sheets/`.
- **Día 3 P2:** `02-reporte-automatico-python/limpiar_reporte.py` lee `ventas_sucias.csv` -> `output/reporte_limpio.xlsx` (3 pestañas: limpio, errores, resumen) + `resumen.txt`.
- **Día 4 P3:** `03-facturacion-conciliacion/conciliar.py` + `generar_facturas.py` -> `output/conciliacion.xlsx` + 3 PDFs ejemplo + `morosos.csv`.
- **Día 5 P4:** `04-crm-tablero/informe_semanal.py` desde `clientes.csv` + `facturas.csv` -> `output/informe_ejecutivo.xlsx` de 1 hoja KPI.
- **Día 6:** pulir `README.md` + `links.txt` + video Loom 60-90s.
- **Día 7:** pegar links en CV, Zonajobs, Computrabajo. 10 postulaciones.

## 6. Definition of Done para cada proyecto

- [ ] Input visible y descargable
- [ ] Script corre con `python <script>.py` sin errores en Windows PowerShell 5.1
- [ ] Output en `output/` con fecha y métrica (ej: "200 filas sucias -> 184 limpias en 8s")
- [ ] README corto del proyecto: problema, herramienta, resultado medible
- [ ] Link agregado a `links.txt` y a `README.md` raíz

## 7. Comandos útiles (PowerShell)

```powershell
# verificar estructura
Get-ChildItem -LiteralPath "C:\Users\rokuy\Desktop\Proyectos\portfolio-admin" -Recurse | Select-Object FullName

# crear entorno y correr P2 (ejemplo)
python -m pip install -r "C:\Users\rokuy\Desktop\Proyectos\portfolio-admin\02-reporte-automatico-python\requirements.txt"
python "C:\Users\rokuy\Desktop\Proyectos\portfolio-admin\02-reporte-automatico-python\limpiar_reporte.py"

# regenerar datasets (solo si se rompen)
python "C:\Users\rokuy\Desktop\Proyectos\portfolio-admin\datasets\generar_datasets.py"
```

## 8. Qué NO hacer

- No inventar experiencia laboral real en empresas. Presentar todo como `Proyecto freelance / simulado`.
- No subir datos personales reales, ni fotos de DNI, ni CBU real.
- No agregar librerías pesadas (django, numpy innecesario, etc). Mantenerlo instalable en 1 minuto por un reclutador técnico.
- No cambiar separador decimal sin documentar. Argentina usa coma en Excel, punto en Python: convertir explícito.
- No dejar links rotos en README. Si Drive aún no es público, poner `PENDIENTE: publicar`.

---
*Dueño: mantiene este archivo actualizado. Todo agente nuevo debe leer este AGENT.md antes de tocar código o datos.*
