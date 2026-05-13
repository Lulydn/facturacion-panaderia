import streamlit as st
import pandas as pd
import io
import re
from datetime import datetime

st.set_page_config(page_title="Facturación Panadería", layout="wide")
st.title("🥐 Generador de Facturación Semanal")

# --- 1. BASE DE DATOS DE PRODUCTOS Y PRECIOS ---
PRODUCT_DB = {
    9054: {'nombre': 'C*PAN PORTEÑO KG', 'iva': 0.10, 'precio_base': 250.0},
    9000: {'nombre': 'C*GALLET.CAMPAÑA KG', 'iva': 0.10, 'precio_base': 110.0},
    9133: {'nombre': 'C*PAN BAGUETTE TRADICIONAL UN', 'iva': 0.10, 'precio_base': 40.0},
    9049: {'nombre': 'C*PAN FLAUTA KG', 'iva': 0.10, 'precio_base': 60.0},
    8153: {'nombre': 'C*ALFAJO.YOYO UNIDAD', 'iva': 0.22, 'precio_base': 50.0},
    9047: {'nombre': 'C*ALFAJO.DE MAICENA', 'iva': 0.22, 'precio_base': 40.0},
    9009: {'nombre': 'C*BIZCOC.KG', 'iva': 0.22, 'precio_base': 460.0},
    9183: {'nombre': 'C*BUDIN INGLES UN', 'iva': 0.22, 'precio_base': 140.0},
    8076: {'nombre': 'C*EMPANA.JAMON Y QUESO UN', 'iva': 0.22, 'precio_base': 50.0},
    8077: {'nombre': 'C*EMPANA.DE CARNE UN', 'iva': 0.22, 'precio_base': 50.0},
    9011: {'nombre': 'C*MASAS FINAS KG', 'iva': 0.22, 'precio_base': 850.0},
    9314: {'nombre': 'C*MILANE.CARNE AL PAN ESPECIAL UN', 'iva': 0.22, 'precio_base': 120.0},
    9070: {'nombre': 'C*MILHOJ.RECTANGULAR UN', 'iva': 0.22, 'precio_base': 90.0},
    9039: {'nombre': 'C*MEDIAL.RELLENA GRANDE UN', 'iva': 0.22, 'precio_base': 80.0},
    9479: {'nombre': 'C*MEDIAL.UNIDAD', 'iva': 0.22, 'precio_base': 30.0},
    9035: {'nombre': 'C*PAN BAGUETTE INTEGRAL UN', 'iva': 0.22, 'precio_base': 40.0},
    9037: {'nombre': 'C*PAN CATALAN KG', 'iva': 0.22, 'precio_base': 250.0},
    9043: {'nombre': 'C*PAN CATALAN INTEGRAL', 'iva': 0.22, 'precio_base': 250.0},
    9050: {'nombre': 'C*PAN DE SANDWICH BLANCO KG', 'iva': 0.22, 'precio_base': 480.0},
    9370: {'nombre': 'C*PAN DE VIENA UN', 'iva': 0.22, 'precio_base': 15.0},
    9180: {'nombre': 'C*PAN DU.500GR', 'iva': 0.22, 'precio_base': 180.0},
    9181: {'nombre': 'C*PAN DU.KG', 'iva': 0.22, 'precio_base': 280.0},
    9488: {'nombre': 'C*PAN FELIPE UNIDAD', 'iva': 0.22, 'precio_base': 50.0},
    9442: {'nombre': 'C*PAN INTEGRAL C/PASAS KG', 'iva': 0.22, 'precio_base': 250.0},
    9012: {'nombre': 'C*PAN RALLADO KG', 'iva': 0.22, 'precio_base': 40.0},
    9053: {'nombre': 'C*PAN TORTUGA KG', 'iva': 0.22, 'precio_base': 16.0},
    9214: {'nombre': 'C*PANCIT.BLANCO S/SAL', 'iva': 0.22, 'precio_base': 120.0},
    9141: {'nombre': 'C*PASTAF.PORCION', 'iva': 0.22, 'precio_base': 90.0},
    9021: {'nombre': 'C*PIZZA 1/4LATA', 'iva': 0.22, 'precio_base': 250.0},
    9020: {'nombre': 'C*PIZZA 1/2LATA', 'iva': 0.22, 'precio_base': 500.0},
    9046: {'nombre': 'C*PLANTI.KG', 'iva': 0.22, 'precio_base': 120.0},
    9161: {'nombre': 'C*PREPIZ.CON MUZZARELLA UN', 'iva': 0.22, 'precio_base': 160.0},
    9162: {'nombre': 'C*PREPIZ.CON GUSTO UN', 'iva': 0.22, 'precio_base': 180.0},
    9215: {'nombre': 'C*PREPIZ.CHICA UN', 'iva': 0.22, 'precio_base': 45.0},
    9195: {'nombre': 'C*ROSCA CHICHARRON KG', 'iva': 0.22, 'precio_base': 80.0},
    9057: {'nombre': 'C*ROSCA COMUN DULCE KG', 'iva': 0.22, 'precio_base': 160.0},
    9143: {'nombre': 'C*ROSCAS TODAS UN', 'iva': 0.22, 'precio_base': 70.0},
    9202: {'nombre': 'C*SANDWI.SURTIDO BANDEJA', 'iva': 0.22, 'precio_base': 190.0},
    9110: {'nombre': 'C*TARTA INDIVIDUAL', 'iva': 0.22, 'precio_base': 90.0},
    9013: {'nombre': 'C*TORTA CUMPLEAÑOS/CASAMIENTO KG', 'iva': 0.22, 'precio_base': 650.0},
    9372: {'nombre': 'C*TORTUG.PARA HAMBURGUESAS 1UN', 'iva': 0.22, 'precio_base': 40.0},
    9042: {'nombre': 'C*PAN MARSELLES KG', 'iva': 0.22, 'precio_base': 250.0},
    9456: {'nombre': 'C*GALLET.MALTEADA DULCE UNIDAD', 'iva': 0.22, 'precio_base': 120.0},
    9201: {'nombre': 'C*SANDWI.JAMON Y QUESO BANDEJA', 'iva': 0.22, 'precio_base': 120.0},
    9056: {'nombre': 'C*ROSCA SALADA COMUN KG', 'iva': 0.22, 'precio_base': 40.0},
    9134: {'nombre': 'C*MASAS SECAS KG', 'iva': 0.22, 'precio_base': 150.0},
    8165: {'nombre': 'C*OJITOS CHICOS UN', 'iva': 0.22, 'precio_base': 100.0},
    9505: {'nombre': 'C*GALLET.PAQUETE', 'iva': 0.22, 'precio_base': 120.0},
    9491: {'nombre': 'C*PAN MA.UNIDAD', 'iva': 0.22, 'precio_base': 60.0},
    8178: {'nombre': 'C*ARROLL.UN VARIOS SABORES', 'iva': 0.22, 'precio_base': 80.0},
    9119: {'nombre': 'C*SANDWI.COMUN UNG', 'iva': 0.22, 'precio_base': 1400.0},
    9188: {'nombre': 'C*SANDWI.MIXTO Y SURTIDO 25UN', 'iva': 0.22, 'precio_base': 350.0},
    9045: {'nombre': 'C*PAN ROSETA KG', 'iva': 0.22, 'precio_base': 140.0},
    9205: {'nombre': 'C*GALLET.MALTEADA AL ACEITE KG', 'iva': 0.22, 'precio_base': 140.0},
    9063: {'nombre': 'C*PIONON.KG', 'iva': 0.22, 'precio_base': 240.0},
    9396: {'nombre': 'C*LUNCH P/5 PERSONAS', 'iva': 0.22, 'precio_base': 2900.0},
    9008: {'nombre': 'C*LUNCH P/5 PERSONAS', 'iva': 0.22, 'precio_base': 130.0},
}

# --- FUNCIÓN AUXILIAR PARA LIMPIAR NÚMEROS ---
def limpiar_numero_uy(valor):
    if pd.isna(valor): return 0.0
    texto = str(valor).replace('.', '').replace(',', '.')
    try:
        return float(texto)
    except ValueError:
        return 0.0

# --- 2. CARGA DE ARCHIVOS ---
uploaded_files = st.file_uploader(
    "Arrastra los archivos CSV de la semana aquí", 
    accept_multiple_files=True, 
    type=['csv', 'txt']
)

if uploaded_files:
    all_data = []
    
    for file in uploaded_files:
        try:
            # LIMPIEZA PROFUNDA
            raw_bytes = file.getvalue()
            clean_bytes = raw_bytes.replace(b'\x00', b'')
            content = clean_bytes.decode('latin-1', errors='ignore')
            lines = content.splitlines()
            
            fecha_str = None
            data_rows = []
            
            for line in lines:
                line = line.strip()
                # A) Buscar Fecha
                if "Fecha contable" in line:
                    try:
                        parts = line.split(':')
                        raw_date = parts[1].strip().split(';')[0].split('\t')[0]
                        digits = "".join(filter(str.isdigit, raw_date))
                        if len(digits) >= 8: fecha_str = digits[:8]
                    except: pass
                
                # B) Buscar Filas
                parts = line.split(';')
                if len(parts) >= 4 and parts[0].strip().isdigit():
                    data_rows.append(line)

            if not fecha_str or not data_rows:
                continue

            # CREAR DATAFRAME
            csv_content = "PLU;Descripcion;Im;Cantidad;UM;Importe;\n" + "\n".join(data_rows)
            df_temp = pd.read_csv(io.StringIO(csv_content), sep=';', dtype=str)
            
            # CORRECCIÓN DE TIPOS
            df_temp['Cantidad'] = df_temp['Cantidad'].apply(limpiar_numero_uy)
            df_temp['Importe'] = df_temp['Importe'].apply(limpiar_numero_uy)
            df_temp['PLU'] = pd.to_numeric(df_temp['PLU'], errors='coerce').fillna(0).astype(int)
            
            fecha_dt = datetime.strptime(fecha_str, "%Y%m%d")
            df_temp['Fecha'] = fecha_dt.strftime("%d/%m/%Y")
            all_data.append(df_temp)
            
        except Exception as e:
            st.error(f"❌ Error en {file.name}: {e}")

    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        
        # --- 3. AUDITORÍA DE PRODUCTOS DESCONOCIDOS ---
        plus_en_archivo = df['PLU'].unique()
        plus_desconocidos = [p for p in plus_en_archivo if p not in PRODUCT_DB]
        
        # --- 4. CÁLCULOS ---
        def get_datos_producto(plu):
            prod = PRODUCT_DB.get(plu)
            if prod:
                return prod['iva'], prod['nombre'], prod.get('precio_base', 0)
            return 0.22, '⚠️ NO REGISTRADO', 0 

        datos_prod = df['PLU'].apply(get_datos_producto)
        
        df['IVA_Porcentaje'] = [x[0] for x in datos_prod]
        df['Nombre_Final'] = [x[1] if x[1] != '⚠️ NO REGISTRADO' else f"⚠️ {row['Descripcion']}" for x, row in zip(datos_prod, df.to_dict('records'))]
        df['Precio_Base_Esperado'] = [x[2] for x in datos_prod]

        # Fórmulas
        df['Venta_Bruta_Sin_IVA'] = df['Importe'] / 0.90
        df['Monto_IVA'] = df['Venta_Bruta_Sin_IVA'] * df['IVA_Porcentaje']
        df['Total_Factura'] = df['Venta_Bruta_Sin_IVA'] + df['Monto_IVA']
        
        # Precio Unitario Real
        df['Precio_Unitario_Real'] = df.apply(
            lambda x: x['Total_Factura'] / x['Cantidad'] if x['Cantidad'] > 0 else 0, axis=1
        )

        # Auditoría de Precio
        df['Diferencia_Precio'] = df['Precio_Unitario_Real'] - df['Precio_Base_Esperado']
        errores_precio = df[
            (df['Precio_Base_Esperado'] > 0) & 
            (df['Diferencia_Precio'].abs() > 5.0)
        ].copy()

        st.success("✅ Archivos procesados")

        # --- A. ALERTAS ---
        if plus_desconocidos:
            st.warning(f"🧐 ¡OJO! Hay {len(plus_desconocidos)} códigos en los archivos que NO están en tu base de datos.")
            st.write("El sistema usó IVA 22% por defecto. Deberías agregarlos a tu código 'PRODUCT_DB':")
            df_desconocidos = df[df['PLU'].isin(plus_desconocidos)][['PLU', 'Descripcion']].drop_duplicates()
            st.table(df_desconocidos)
            st.divider()

        if not errores_precio.empty:
            st.error(f"💸 ¡ATENCIÓN! {len(errores_precio)} ventas tienen diferencia de precio.")
            st.dataframe(
                errores_precio[['Fecha', 'Nombre_Final', 'Precio_Base_Esperado', 'Precio_Unitario_Real', 'Diferencia_Precio']].style.format({
                    'Precio_Base_Esperado': "${:.2f}",
                    'Precio_Unitario_Real': "${:.2f}",
                    'Diferencia_Precio': "${:.2f}"
                }),
                use_container_width=True
            )
            st.divider()

        # --- B. TOTALES ---
        col1, col2 = st.columns(2)
        total_global = df['Total_Factura'].sum()
        col1.metric("💰 TOTAL A FACTURAR", f"$ {total_global:,.2f}")
        col2.metric("📦 CANTIDAD DE ÍTEMS", f"{int(df['Cantidad'].sum())}")

        # --- C. TABLA RESUMEN (CORREGIDO) ---
        # Redondeamos a 2 decimales para que Pandas agrupe bien y no se confunda con variaciones de centésimos
        df['Precio_Agrupado'] = df['Precio_Unitario_Real'].round(2)
        
        # Ahora agrupamos incluyendo el Precio_Agrupado. Si hay 2 precios distintos, creará 2 filas.
        pivot = df.groupby(['PLU', 'Nombre_Final', 'Precio_Agrupado']).agg({
            'Cantidad': 'sum',
            'Total_Factura': 'sum'
        }).reset_index()
        
        # Función para detectar si la fila es del precio nuevo o viejo
        def determinar_estado_precio(row):
            base = PRODUCT_DB.get(row['PLU'], {}).get('precio_base', 0)
            if base > 0 and abs(row['Precio_Agrupado'] - base) > 5.0:
                return "⚠️ MODIFICADO"
            return "✅ BASE"

        pivot['Tipo_Precio'] = pivot.apply(determinar_estado_precio, axis=1)

        # Renombramos columnas para mostrar
        pivot.rename(columns={
            'Total_Factura': 'TOTAL ($)', 
            'Precio_Agrupado': 'PRECIO UNIT. ($)'
        }, inplace=True)

        # Reordenamos las columnas para que quede prolijo
        pivot = pivot[['PLU', 'Nombre_Final', 'Tipo_Precio', 'PRECIO UNIT. ($)', 'Cantidad', 'TOTAL ($)']]

        st.subheader("📋 Detalle para Factura")
        st.dataframe(
            pivot.style.format({'TOTAL ($)': "${:,.2f}", 'PRECIO UNIT. ($)': "${:,.2f}"}), 
            use_container_width=True
        )

        # --- D. DESCARGA ---
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            pivot.to_excel(writer, sheet_name='Resumen_Factura', index=False)
            if plus_desconocidos:
                df[df['PLU'].isin(plus_desconocidos)].to_excel(writer, sheet_name='PRODUCTOS_NUEVOS', index=False)
            if not errores_precio.empty:
                errores_precio.to_excel(writer, sheet_name='ERRORES_PRECIO', index=False)
            df.to_excel(writer, sheet_name='Detalle_Completo', index=False)
            
        st.download_button(
            label="📥 Descargar Excel Completo",
            data=buffer,
            file_name="Facturacion_Controlada.xlsx",
            mime="application/vnd.ms-excel"
        )