from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime

def configurar_webdriver():
    service = Service('C:/chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(15)
    return driver

def construir_url(fecha_inicial, fecha_final):
    url_base = "https://www.bcn.gob.ni/IRR/tipo_cambio_mensual/mes.php"
    parametros = f"?Fecha_inicial={fecha_inicial}&Fecha_final={fecha_final}"
    return url_base + parametros

def extraer_datos(driver, url_completa):
    driver.get(url_completa)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr'))
        )
        filas = driver.find_elements(By.XPATH, '/html/body/table/tbody/tr')
        datos = []
        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, 'td')
            datos_fila = [celda.text for celda in celdas]
            datos.append(datos_fila)
        return datos
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []

def escribir_csv(datos):
    with open('C:/Users/yesal/Desktop/Python/scrapping/TasaCambioNic/datos.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        for fila in datos:
            escritor_csv.writerow(fila)

def validar_formato_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def main():
    driver = configurar_webdriver()
    print("El formato de consulta es: yyyy-mm-dd")
    
    fecha_inicial = input("Ingresa la fecha inicial: ")
    while not validar_formato_fecha(fecha_inicial):
        print("La fecha inicial no cumple con el formato yyyy-mm-dd. Por favor, intenta de nuevo.")
        fecha_inicial = input("Ingresa la fecha inicial: ")
    
    fecha_final = input("Ingresa la fecha final: ")
    while not validar_formato_fecha(fecha_final):
        print("La fecha final no cumple con el formato yyyy-mm-dd. Por favor, intenta de nuevo.")
        fecha_final = input("Ingresa la fecha final: ")
    
    url_completa = construir_url(fecha_inicial, fecha_final)
    datos = extraer_datos(driver, url_completa)
    if datos:
        escribir_csv(datos)
    driver.quit()

if __name__ == "__main__":
    main()