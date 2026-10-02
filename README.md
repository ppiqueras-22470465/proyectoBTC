# 📈 Preprocesamiento de Datos de Bitcoin para Machine Learning (BTCUSDT)

Este repositorio contiene un *pipeline* automatizado en Python diseñado para procesar, limpiar y enriquecer datos históricos de Bitcoin (BTCUSDT) con intervalos de 15 minutos. El objetivo del script es generar un dataset robusto mediante técnicas de ingeniería de características (*feature engineering*), dejándolo 100% preparado para la fase de entrenamiento de modelos predictivos de Machine Learning.

> **Nota del Proyecto:** Este script se enfoca exclusivamente en el tratamiento matemático y temporal de los datos. No incluye la fase de entrenamiento (training) del modelo.

## 🚀 Características del Pipeline (Flujo de Trabajo)

El código ejecuta de forma secuencial las siguientes fases de tratamiento:

1. **Extracción y Formateo (`extraerDatos` y `correguirFecha`):**
   - Carga de los datos brutos del par BTCUSDT.
   - Conversión estandarizada de la columna temporal a formato *datetime* (UTC).
   - Filtrado exacto del rango de estudio: **1 al 31 de agosto de 2026**.

2. **Validación de Continuidad (`revisarTiempo`):**
   - Análisis de saltos temporales mediante el cálculo de diferencias (`.diff()`).
   - Verificación matemática de que todos los registros mantienen un intervalo constante de 15 minutos, sin pérdida de datos.

3. **Ingeniería de Características (*Feature Engineering*):**
   - **Lag Features (`lagFeatures`):** Creación de variables de retardo para evaluar el impacto histórico a 1 periodo (15 min), 4 periodos (1 hora) y 96 periodos (1 día).
   - **Rolling Statistics (`rollingStatistics`):** Cálculo de la media móvil (`rolling_mean_4`) y la desviación típica (`rolling_std_4`) basándose en una ventana de 4 periodos para capturar la volatilidad reciente.

4. **Creación de la Variable Objetivo (`crearTarget`):**
   - Construcción de la columna `target` utilizando el precio de cierre del periodo futuro inmediato (`.shift(-1)`).
   - Limpieza automática de todos los registros nulos (`NaN`) generados en los extremos del dataset por los desplazamientos temporales.

5. **Exportación:**
   - El resultado final se exporta automáticamente a un archivo `dataset_limpio.csv`, sin índices innecesarios, listo para su ingesta en cualquier algoritmo predictivo.

## 🛠️ Tecnologías y Librerías

- **Lenguaje:** Python 3
- **Manipulación de Datos:** Pandas

## ⚙️ Cómo ejecutar el proyecto

1. Asegúrate de tener instalado Python y la librería Pandas en tu entorno:
   ```bash
   pip install pandas
