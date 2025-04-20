# import
import time
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver

# Defino constantes
user = 
clave = 

fecha_lejana = '01/06/2022'

droguerias = ['DROGUERIA META S A', 'GRUPO SUD LATIN S.A.', 'EQUS FARMA S.R.L.', 'DROGUERIA INSUTRACK S. R. L.','ONCO LIFE S.R.L.','MONROE AMERICANA SOCIEDAD ANONIMA','EFSA S.A.','GLOBAL MED S A','CO FA LO ZA LDA COOPERATIVA DE FARMACIAS DE L DE ZAMORA','ASISTENCIA FARMACEUTICA S A','Todas']

path0 = '/html/body/form/div/table/tbody/'
path1 = '/html/body/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/form/table/tbody/tr/td[2]/table/tbody/'
path2 = '/html/body/div[2]/table/tbody/tr/td/div/form/table/tbody/tr[2]/td/div[1]/'

"""
class Listado:
    def __init__(self, id, nComprobante, nAfil, nObra):
        self.id = id
        self.nComprobante = nComprobante
        self.nAfil = nAfil
        self.nObra = nObra
"""

def inicio(driver):
    # entramos a la pagina con user y clave
    driver.get("http://servicios.cofa.org.ar/ncr/")
    driver.find_element("xpath", f'{path0}tr[1]/td[2]/select/option[9]').click()
    driver.find_element("xpath", f'{path0}tr[2]/td[2]/input').send_keys(user)
    driver.find_element("xpath", f'{path0}tr[3]/td[2]/input[1]').send_keys(clave)
    driver.find_element("xpath", f'{path0}/tr[3]/td[2]/input[2]').click()

    #  entro a la seccion de trazas
    driver.find_element("xpath", f'{path0}tr[1]/td/div[1]/table[2]/tbody/tr/td[1]/a').click()

def guardar_datos(driver):
    try:
        archivo = open("datos.txt", "w")
    except:
        messagebox.showerror("Error", "Error al abrir el archivo datos.txt")
        sys.exit()

    remedios = driver.execute_script('return document.querySelector("body>div>table>tbody>tr>td>div>table>tbody>tr:nth-child(2)>td>div>div>div>form>table>tbody").getElementsByTagName("tr"); ')

    for remedio in remedios[1:]:
        remedio.find_element("xpath", 'td[1]/input').click()
        numero = remedio.find_element("xpath", "td[4]").text.split('\n')[1]
        archivo.write(f'{numero}\n')

    archivo.close()

def traer_datos(driver, drogueria):

    # Selecciono la fecha
    driver.find_element("xpath",f'{path1}tr[1]/td[2]/p/input').clear()
    driver.find_element("xpath",f'{path1}tr[1]/td[2]/p/input').send_keys(fecha_lejana)
    driver.find_element("xpath", f'{path1}tr[2]/td[3]/input').click()
    time.sleep(1)

    # Trazo todos o algunos
    if drogueria != 'Todas':
        driver.find_element("xpath", f'{path1}tr[2]/td[2]/select/option[{droguerias.index(drogueria)+2}]').click()
        time.sleep(1)
        driver.find_element("xpath", f'{path1}tr[3]/td[3]/input').click()
        guardar_datos(driver)
    else:
        guardar_datos(driver)

def trazar(driver):
    try:
        archivo = open("datos.txt", "r")
    except:
        messagebox.showerror("Error", "Error al abrir el archivo datos.txt")
        sys.exit()

    numeros = archivo.readlines()

    for numero in numeros:

        try:
            driver.switch_to.parent_frame()
            driver.switch_to.default_content()

            driver.find_element("xpath", f'{path2}table[1]/tbody/tr/td[2]/input').send_keys(numero.split("\n")[0])
            driver.find_element("xpath", f'{path2}table[1]/tbody/tr/td[3]/input').click()

            time.sleep(2)

        # Seteamos los valores de las trazas #

            # Tipo de comprobante
            driver.find_element("xpath", f'{path2}table[2]/tbody/tr[1]/td[2]/select/option[5]').click()
            # N° de transaccion
            driver.find_element("xpath", f'{path2}table[2]/tbody/tr[1]/td[6]/input').send_keys(1)
            # Obra social
            driver.find_element("xpath", f'{path2}table[2]/tbody/tr[2]/td[2]/select/option[545]').click()
            # N° Afiliado
            driver.find_element("xpath", f'{path2}table[2]/tbody/tr[3]/td[2]/input').send_keys(1)

            iframes = driver.execute_script('return document.getElementsByTagName("iframe"); ')

        # Recorremos cada remedio y lo validamos #
            for iframe in iframes:
                driver.switch_to.parent_frame()
                driver.switch_to.frame(driver.find_element("xpath", f'{path2}/table[3]/tbody/tr[2]/td[6]/iframe'))
                driver.execute_script('trazar31()')
                time.sleep(4)
            time.sleep(3)

        except:
            messagebox.showerror('Error', f'Error al cargar la traza {numero}')
            archivo.close()
            sys.exit()

    archivo.close()

def main():

    drogueria = listaDesplegble1.get()

    carga = listaDesplegble2.get()

    #cierro la visual de la app
    root.quit()

    #Inicializo el web driver
    driver = webdriver.Chrome("chromedriver.exe")

    # Abro la pagina
    inicio(driver)

    time.sleep(3)

    # Cambio a la segunda pagina
    handles = driver.window_handles
    driver.switch_to.parent_frame()
    driver.switch_to.default_content()
    driver.switch_to.window(handles[1])

    # Lleno con todas las trazas el archivo
    if carga == 'Automatico':
        traer_datos(driver, drogueria)
        driver.find_element("xpath", '/html/body/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/div/form/input').click()
        time.sleep(6)

    time.sleep(2)

    # Cambio a la seccion para trazar
    driver.find_element("xpath", f'/html/body/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/a[1]').click()

    trazar(driver)


####################################################################
################## Parte visual de la aplicacion ###################
####################################################################

# creamos la pestaña
root = tk.Tk()
root.resizable(width=0, height=0)
root.title('Trazamed')

# configuramos la pestaña
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.config(background="#ECF0F1")
canvas1.pack()

# box text 1
label1 = tk.Label(root, text='Trazabilidad medicamentos cofa')
label1.config(font=('helvetica', 20), background="#AED6F1", width=60, height=2, pady=1)
canvas1.create_window(200, 25, window=label1)

# box text 2
label2 = tk.Label(root, text='Seleccionar drogueria:')
label2.config(font=('helvetica', 12), background="#F2F3F4")
canvas1.create_window(200, 90, window=label2)

# crear lista desplegable con las dif droguerias
listaDesplegble1 = ttk.Combobox(
    state = "readonly",
    values = droguerias
)
listaDesplegble1.config(width=40)
canvas1.create_window(200, 130, window=listaDesplegble1)

# box text 3
label2 = tk.Label(root, text='Cargar datos:')
label2.config(font=('helvetica', 12), background="#F2F3F4")
canvas1.create_window(200, 165, window=label2)

# crear lista desplegable para saber si los datos son cargados manuales o no
listaDesplegble2 = ttk.Combobox(
    state = "readonly",
    values = ['Manual', 'Automatico']
)
listaDesplegble2.config(width=40)
canvas1.create_window(200, 195, window=listaDesplegble2)

# boton para trazar
button1 = tk.Button(text='Trazar', command=main)
button1.config(width=10, background="#D5D8DC")
canvas1.create_window(200, 265, window=button1)

root.mainloop()

####################################################################
####################################################################
####################################################################
