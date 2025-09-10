# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

"""
Taller 3
Alejandro Herrera Andrade
Joan Sebastían Schick Reyes
Julian Mauricio Romero Cuevas
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import pearsonr
import numpy as np



# Cargar el archivo CSV 
file_path = r"C:\Users\Lenovo\Documents\2025\2025-2\Haciendo Economía\PROYECTO-2\Raw Data\NH.Ts+dSST.csv"
df = pd.read_csv(file_path, skiprows=1)


"""
Pregunta 1.1.2, 1.1.3, 1.1.4


(1.1.2)	Elige un mes y construye un gráfico de línea con la anomalía de temperatura
 promedio en el eje vertical y el tiempo (desde 1880 hasta el último año disponible)
 en el eje horizontal.
"""

# 2. Seleccionar el mes a graficar 
mes = "Jan"

# Convertir la columna a numérica 
df[mes] = pd.to_numeric(df[mes], errors="coerce")

# 3. Graficar 
plt.figure(figsize=(12,6))
plt.plot(df["Year"], df[mes], color="blue", label=mes)

# Línea horizontal en y=0 con etiqueta
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.text(df["Year"].min()+3, 0.1, "Promedio de 1951 a 1980", color="red")

# Etiquetas y título
plt.xlabel("Año")
plt.ylabel("Anomalía de temperatura (°C)")
plt.title(f"Anomalía de temperatura en {mes} (1880 - último año disponible)")
plt.legend()

plt.show()


"""
(1.1.3)	Ahora, otro gráfico pero con los promedios de cada estación (una línea por estación).
  Las columnas DJF, MAM, JJA, SON contienen dicha información. Por ejemplo, 
  MAM es el promedio de los meses Marzo, Abril y Mayo.
"""


# 2. Seleccionar columnas 
# Estaciones: DJF (Dic-Ene-Feb), MAM (Mar-May), JJA (Jun-Ago), SON (Sep-Nov)
cols = ["DJF", "MAM", "JJA", "SON"]

# Convertir a numérico 
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

# 3. Graficar 
plt.figure(figsize=(12,6))

# Graficar cada estación con una línea
for col in cols:
    plt.plot(df["Year"], df[col], label=col)

# Línea horizontal en y=0 con etiqueta
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.text(df["Year"].min()+2, 0.2, "Promedio de 1951 a 1980", color="red")

# Etiquetas y título
plt.xlabel("Año")
plt.ylabel("Anomalía de temperatura (°C)")
plt.title("Anomalías de temperatura promedio por estación (1880 - último año disponible)")
plt.legend(title="Estaciones")

plt.show()


"""
(1.1.4)	Ahora hagamos una gráfica con los promedios de las anomalías anuales.
      Esta información está en las columnas J-D
"""

df["J-D"] = pd.to_numeric(df["J-D"], errors="coerce")

# 3. Graficar 
plt.figure(figsize=(12,6))
plt.plot(df["Year"], df["J-D"], color="blue", label="Anual (J-D)")

# Línea horizontal en y=0 con etiqueta
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.text(df["Year"].min()+2, 0.05, "Promedio de 1951 a 1980", color="red")

# Etiquetas y título
plt.xlabel("Año")
plt.ylabel("Anomalía de temperatura (°C)")
plt.title("Anomalía de temperatura promedio anual (1880 - último año disponible)")
plt.legend()

plt.show()


"""""
1.2.1

Crea dos tablas de frecuencias similares a la Figura 1.6 para los años 
1951–1980 y 1981–2010. 


1.2.2

Con las tablas de frecuencias: 
- Construye dos histogramas (1951–1980 y 1981–2010) mostrando la distribución 
de anomalías de temperatura. 
"""
# Seleccionar solo columnas necesarias
df1 = df[["Year", "J-D"]].copy()

# Convertir a numérico (ignorar "*")
df1["J-D"] = pd.to_numeric(df1["J-D"], errors="coerce")

# Filtrar periodos con .copy() para evitar warnings
periodo1 = df1[(df1["Year"] >= 1951) & (df1["Year"] <= 1980)].copy()
periodo2 = df1[(df1["Year"] >= 1981) & (df1["Year"] <= 2010)].copy()

# Redondear anomalías a pasos de 0.05 °C
periodo1["Anom_Rounded"] = periodo1["J-D"].round(2)
periodo2["Anom_Rounded"] = periodo2["J-D"].round(2)

# Contar frecuencias
tabla1 = periodo1["Anom_Rounded"].value_counts().sort_index()
tabla2 = periodo2["Anom_Rounded"].value_counts().sort_index()

# Convertir en DataFrames estilo tabla de frecuencias
tabla1_df = pd.DataFrame({
    "Range of anomaly (°C)": tabla1.index,
    "Frequency (1951–1980)": tabla1.values
})
tabla2_df = pd.DataFrame({
    "Range of anomaly (°C)": tabla2.index,
    "Frequency (1981–2010)": tabla2.values
})

print("Tabla de frecuencias 1951–1980")
print(tabla1_df.to_string(index=False))

print("\nTabla de frecuencias 1981–2010")
print(tabla2_df.to_string(index=False))

# Construir los histogramas
fig, axes = plt.subplots(1, 2, figsize=(14,6), sharey=True)

# Histograma 1951–1980
axes[0].hist(periodo1["J-D"], bins=10, color="skyblue", edgecolor="black")
axes[0].set_title("Distribución de anomalías 1951–1980")
axes[0].set_xlabel("Anomalía de temperatura (°C)")
axes[0].set_ylabel("Frecuencia")
axes[0].axvline(periodo1["J-D"].mean(), color="red", linestyle="--", 
                label=f"Media: {periodo1['J-D'].mean():.2f}")
axes[0].legend()

# Histograma 1981–2010
axes[1].hist(periodo2["J-D"], bins=10, color="lightgreen", edgecolor="black")
axes[1].set_title("Distribución de anomalías 1981–2010")
axes[1].set_xlabel("Anomalía de temperatura (°C)")
axes[1].axvline(periodo2["J-D"].mean(), color="red", linestyle="--", 
                label=f"Media: {periodo2['J-D'].mean():.2f}")
axes[1].legend()

plt.tight_layout()
plt.show()

"""
1.2.3

El artículo del New York Times clasifica el tercio inferior (1er al 3er decil) 
como “frío” y el tercio superior (7º al 10º decil) como “caliente”. 
- Usa la función np.quantile (numpy) en Python para encontrar los valores 
correspondientes a los deciles 3 y 7 en 1951–1980. 

"""

# Convertir a numérico (algunos valores son "*")
df["J-D"] = pd.to_numeric(df["J-D"], errors="coerce")

periodo1 = df[(df["Year"] >= 1951) & (df["Year"] <= 1980)]["J-D"].dropna()

# Calcular deciles 3 (30%) y 7 (70%)
d3 = np.quantile(periodo1, 0.3)
d7 = np.quantile(periodo1, 0.7)

print(f"Decil 3 (30%): {d3:.2f} °C")
print(f"Decil 7 (70%): {d7:.2f} °C")

# (Opcional) Más estadísticas
print(f"Mínimo: {periodo1.min():.2f} °C")
print(f"Mediana: {periodo1.median():.2f} °C")
print(f"Máximo: {periodo1.max():.2f} °C")



"""
1.2.4

Usando los valores de la Pregunta 3, cuenta cuántas anomalías se consideran 
“calientes” en 1981–2010 y exprésalo como porcentaje. 
- ¿Esto sugiere que experimentamos temperaturas altas más frecuentemente 
en 1981–2010? 

"""
# Filtrar periodos
periodo1 = df[(df["Year"] >= 1951) & (df["Year"] <= 1980)]["J-D"].dropna()
periodo2 = df[(df["Year"] >= 1981) & (df["Year"] <= 2010)]["J-D"].dropna()

# Calcular deciles de referencia (1951–1980)
d3 = np.quantile(periodo1, 0.3)
d7 = np.quantile(periodo1, 0.7)

# Contar años "calientes" en 1981–2010
calientes = (periodo2 >= d7).sum()
total = len(periodo2)
porcentaje = (calientes / total) * 100

print(f"Años calientes en 1981–2010: {calientes} de {total} ({porcentaje:.1f}%)")



"""
1.2.5

El artículo discute si las temperaturas se han vuelto más variables con el 
tiempo. 
- Calcula la media y varianza de las temperaturas en cada estación 
(DJF, MAM, JJA, SON) para 1921–1950, 1951–1980 y 1981–2010. 

"""
# Convertir a numérico
for col in ["DJF", "MAM", "JJA", "SON"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Definir periodos
periodos = {
    "1921-1950": (1921, 1950),
    "1951-1980": (1951, 1980),
    "1981-2010": (1981, 2010)
}

# Crear tabla de medias y varianzas
resultados = {}

for nombre, (inicio, fin) in periodos.items():
    subset = df[(df["Year"] >= inicio) & (df["Year"] <= fin)]
    medias = subset[["DJF", "MAM", "JJA", "SON"]].mean()
    varianzas = subset[["DJF", "MAM", "JJA", "SON"]].var()
    resultados[nombre] = pd.DataFrame({
        "Media": medias,
        "Varianza": varianzas
    })

# Unir resultados en una sola tabla
tabla_final = pd.concat(resultados, axis=1)
print(tabla_final)


"""
1.3.3

Grafica una línea con los niveles de CO₂ (interpolated y trend) en el eje vertical
y el tiempo (desde enero de 1960) en el eje horizontal.
- Etiqueta los ejes, incluye la leyenda y titula el gráfico.
- ¿Qué sugiere este gráfico sobre la relación entre CO₂ y tiempo?
"""

# 2) Cargar archivo Excel 
co2_data = pd.read_excel(r"C:\Users\Lenovo\Documents\2025\2025-2\Haciendo Economía\PROYECTO-2\Created Data\CO2.xlsx")

# 3) Limpiar nombres de columnas por si tienen espacios
co2_data.columns = [c.strip() for c in co2_data.columns]

# 4) Convertir las columnas numéricas 
for col in ["Monthly average", "Interpolated", "Trend"]:
    if col in co2_data.columns:
        co2_data[col] = pd.to_numeric(
            co2_data[col].astype(str).str.replace(",", ".", regex=False),
            errors="coerce"
        )

# 5) Crear columna de fecha (día 1 de cada mes)
co2_data["Date"] = pd.to_datetime(dict(year=co2_data["Year"].astype(int),
                                       month=co2_data["Month"].astype(int),
                                       day=1))

# 6) Filtrar desde enero de 1960 y quitar filas sin datos
co2_data = co2_data[co2_data["Date"] >= "1960-01-01"].dropna(subset=["Interpolated", "Trend"])

# 7) Graficar
plt.figure(figsize=(11, 5.5))
plt.plot(co2_data["Date"], co2_data["Interpolated"], label="Interpolated (mensual)", alpha=0.7)
plt.plot(co2_data["Date"], co2_data["Trend"], label="Trend (tendencia suavizada)", linewidth=2, color="red")

# 8) Dar formato al gráfico
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(base=5))   # marca cada 5 años
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xlabel("Tiempo (años, desde 1960)")
plt.ylabel("CO₂ (ppm)")
plt.title("CO₂ atmosférico en Mauna Loa: valores mensuales interpolados y tendencia")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.show()


"""
1.3.4
Elige un mes y añade los datos de la tendencia del CO₂ al conjunto de anomalías de temperatura de la Parte 1.1. 
- Haz un diagrama de dispersión (CO₂ en el eje vertical, anomalía de temperatura en el horizontal). 
- Calcula el coeficiente de correlación de Pearson. 
- Interpreta el resultado y discute sus limitaciones. 
"""

# Procesar temperaturas (solo Enero)
temp_jan = df[["Year", "Jan"]].copy()
temp_jan.rename(columns={"Jan": "Temp_Anomaly"}, inplace=True)

# Filtrar CO2 solo Enero 
co2_jan = co2_data[co2_data["Month"] == 1][["Year", "Trend"]].copy()
co2_jan.rename(columns={"Trend": "CO2_Trend"}, inplace=True)

# Hacer merge por año
merged = pd.merge(temp_jan, co2_jan, on="Year", how="inner")

# Diagrama de dispersión 
plt.figure(figsize=(8,6))
plt.scatter(merged["Temp_Anomaly"], merged["CO2_Trend"], alpha=0.7)
plt.title("CO₂ vs Temp Anomaly (January)")
plt.xlabel("Temperature Anomaly (°C)")
plt.ylabel("CO₂ Trend (ppm)")
plt.grid(True)
plt.show()

# Calcular correlación de Pearson 
correlation, p_value = pearsonr(merged["Temp_Anomaly"], merged["CO2_Trend"])
print(f"Coeficiente de correlación de Pearson: {correlation:.3f}")
print(f"Valor p: {p_value:.3e}")

# Guardar el merge en un Excel 
output_path = r"C:\Users\Lenovo\Documents\2025\2025-2\Haciendo Economía\PROYECTO-2\Created Data\merged.xlsx"
merged.to_excel(output_path, index=False)








