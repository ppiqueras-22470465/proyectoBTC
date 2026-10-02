import pandas as pd

archivo = "BTCUSDT_15m_2026-09-28.csv"
archivo_ordenado = ""
def extraerDatos():
    try:
         archivo_ordenado = pd.read_csv(archivo)
         return archivo_ordenado
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return archivo_ordenado

def correguirFecha(archivo_ordenado):
    if(archivo_ordenado.empty != True):
        archivo_ordenado['timestamp'] = pd.to_datetime(archivo_ordenado['timestamp'], utc=True)
        archivo_ordenado_fecha = archivo_ordenado[(archivo_ordenado['timestamp'] >= '2026-08-01 00:00:00') & (archivo_ordenado['timestamp'] <= '2026-08-31 23:45:00')]
        archivo_ordenado_fecha = archivo_ordenado_fecha.sort_values(by=['timestamp'], ascending=True)
        revisarTiempo(archivo_ordenado_fecha)
        return archivo_ordenado_fecha
    else:
        return archivo_ordenado

def revisarTiempo(archivo_ordenado_fecha):
    diferencia = archivo_ordenado_fecha['timestamp'].diff()
    if(diferencia.dropna()== pd.Timedelta(minutes=15)).all():
        print("-----------------------------------------")
        print("| Los datos no tiene saltos temporales. |")
        print("-----------------------------------------")

    else:
        print("--------------------------------------")
        print("| Los datos tiene saltos temporales. |")
        print("--------------------------------------")

# Lag Features
def lagFeatures(archivo_ordenado_fecha):
    archivo_ordenado_fecha ['close_lag_1'] = archivo_ordenado_fecha['close'].shift(1)
    archivo_ordenado_fecha['close_lag_4'] = archivo_ordenado_fecha['close'].shift(4)
    archivo_ordenado_fecha['close_lag_96'] = archivo_ordenado_fecha['close'].shift(96)
    return archivo_ordenado_fecha
# Rolling Statistics
def rollingStatistics(archivo_ordenado_fecha):
    archivo_ordenado_fecha['rolling_mean_4'] = archivo_ordenado_fecha['close_lag_1'].rolling(4).mean() # Media móvil
    archivo_ordenado_fecha['rolling_std_4'] = archivo_ordenado_fecha['close_lag_1'].rolling(4).std() # Desviación típica
    return archivo_ordenado_fecha

def crearTarget(archivo_ordenado_fecha):
    archivo_ordenado_fecha['target'] = archivo_ordenado_fecha['close'].shift(-1)# Cojo el dato futuro y lo pongo en la fila actual
    return archivo_ordenado_fecha.dropna()


# Antes de tratar los datos
print(extraerDatos())
# Después de tratarlos
df = extraerDatos()
df = correguirFecha(df)
df = lagFeatures(df)
df = rollingStatistics(df).dropna() # Con esto quito los NaN que hay en las 96 filas de nulos
df = crearTarget(df)
# Genero los datos ya limpios y con las tablas requeridas
df.to_csv('dataset_limpio.csv', index=False)
print(df)