# Día 2 - P1 Stock y Ventas en Sheets

## Objetivo entrevista
Poder decir: "Armé un control de stock con 50 SKU, 200 ventas, alertas de reposición y dashboard por mes/vendedor/categoría".

## Estructura Sheets (5 hojas)
1. `LEEME` - 5 líneas: qué es, datos simulados, cómo leer Dashboard
2. `Productos` - importar `datasets/productos.csv`
3. `Ventas` - importar `datasets/ventas_limpias.csv`
4. `Movimientos` - carga manual: fecha | codigo | tipo (ENTRADA/SALIDA) | cantidad | motivo
5. `Dashboard` - tabla dinámica + gráficos + alertas

## Fórmulas clave (pegar en español AR, separador ; )
En `Productos`:
- Stock teórico: `=C2+SUMAR.SI(Movimientos!B:B;A2;Movimientos!D:D)` donde C=stock inicial ajustado por tipo. Mejor: separar ENTRADA/SALIDA:
  - Entradas: `=SUMAR.SI.CONJUNTO(Movimientos!D:D;Movimientos!B:B;A2;Movimientos!C:C;"ENTRADA")`
  - Salidas: `=SUMAR.SI.CONJUNTO(Movimientos!D:D;Movimientos!B:B;A2;Movimientos!C:C;"SALIDA") + SUMAR.SI(Ventas!E:E;A2;Ventas!G:G)`
  - Stock actual calc: `=G2+H2-I2` (adaptar columnas)
- Alerta: `=SI(J2<=H2;"REPONER";"OK")` donde J=stock calc, H=stock_minimo
- Precio con IVA: `=F2*1,21`
- Buscar nombre: `=XLOOKUP(A2;Productos!A:A;Productos!B:B;"NO EXISTE")` o `=BUSCARV(A2;Productos!A:B;2;FALSO)`

En `Ventas`:
- Mes: `=TEXTO(B2;"AAAA-MM")` si B es fecha
- Total check: `=G2*H2`

QUERY ejemplo en Dashboard:
```
=QUERY(Ventas!A:K;"select K, sum(I) where A is not null group by K label K 'Vendedor', sum(I) 'Total ARS'";1)
=QUERY(Ventas!A:K;"select B, sum(I) group by B order by B label B 'Mes'";0) con columna mes auxiliar
```

## Validaciones
- Productos!C:C (categoría): lista Librería,Limpieza,Oficina,Electrónica,Almacén
- Movimientos!C:C: lista ENTRADA,SALIDA
- Ventas!J:J (medio_pago): lista Efectivo,Transferencia,Mercado Pago,Tarjeta
- Código: `=CONTAR.SI(Productos!A:A;A2)=1` como validación personalizada

## Formato condicional
- Productos: si stock_calc <= stock_minimo -> rojo claro + texto REPONER
- Ventas: duplicados id_venta -> `=CONTAR.SI($A:$A;$A1)>1` amarillo
- Dashboard KPI: semáforo

## Tabla dinámica (Insertar > Tabla dinámica)
- Filas: Mes | Columnas: Categoría | Valores: SUM Total | Filtro: Vendedor
- Segunda: Filas Vendedor, Valores SUM Total + COUNT id_venta (ticket promedio = total / cantidad)

## Entregable
- Link lector en links.txt -> SHEETS_STOCK_VENTAS
- 2 capturas PNG aquí: dashboard.png + alerta_stock.png
