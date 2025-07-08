# import
import time
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Defino constantes
user = 
clave = 

#Inicializo el web driver
driver = webdriver.Chrome("chromedriver.exe")

def inicio(driver):
    # entramos a la pagina con user y clave
    path0 = '/html/body/div[1]/form/table/tbody/'
    driver.get("https://principal.cofa.org.ar/")
    driver.find_element("xpath", f'{path0}tr[1]/td[2]/input').send_keys(user)
    driver.find_element("xpath", f'{path0}tr[2]/td[2]/input').send_keys(clave)
    driver.find_element("xpath", f'{path0}tr[3]/td[2]/input[2]').click()

    #  entro a la seccion de trazas
    driver.find_element("xpath", f'/html/body/div[3]/table/tbody/tr[3]/td/a').click()
    driver.find_element("xpath", f'/html/body/div[3]/table/tbody/tr[3]/td/ul/li[7]').click()
    

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

def traer_datos(drogeria, drogerias):

    index = drogerias.index(drogeria)+1
    path1 = '/html/body/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/form/table/tbody/tr/td[2]/table/tbody/'                
    driver.find_element("xpath", f'{path1}tr[2]/td[2]/select/option[{index}]').click()
    time.sleep(1)
    driver.find_element("xpath", f'{path1}tr[3]/td[3]/input').click()

    guardar_datos(driver)

def trazar(drogueria, drogerias):

    if forma.get() == "automatico":
        # Lleno con todas las trazas el archivo
        traer_datos(drogueria, drogerias)
        driver.find_element("xpath", '/html/body/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/div/form/input').click()
        time.sleep(3)

    # Cambio a la seccion para trazar 
    driver.find_element("xpath", f'/html/body/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/a[1]').click()

    try:
        archivo = open("datos.txt", "r")
    except:
        messagebox.showerror("Error", "Error al abrir el archivo datos.txt")
        sys.exit()

    numeros = archivo.readlines()
    path2 = '/html/body/div[2]/table/tbody/tr/td/div/form/table/tbody/tr[2]/td/div[1]/'

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
                try:
                    driver.switch_to.frame(driver.find_element("xpath", f'{path2}/table[3]/tbody/tr[2]/td[6]/iframe'))
                    driver.execute_script('trazar31()')
                    time.sleep(4)
                except:
                    driver.find_element("xpath", f'/html/body/div/div[2]/button[1]').click()

            time.sleep(3)

        except:
            messagebox.showerror('Error', f'Error al cargar la traza {numero}')

    messagebox.showinfo(title="FIN DE TRAZA", message="Se termino de trazar")
    archivo.close()
    sys.exit()
def main():

    # Abro la pagina
    inicio(driver)

    time.sleep(3)

    # Seteo la fecha de inicio y fin de la traza
    path1 = '/html/body/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/form/table/tbody/tr/td[2]/table/tbody/'
    fechaIn = calIn.get_date()
    driver.find_element("xpath", f'{path1}tr[1]/td[2]/p/input').clear()
    driver.find_element("xpath", f'{path1}tr[1]/td[2]/p/input').send_keys(parse_fecha(fechaIn))
    fechaFin = calFin.get_date()
    driver.find_element("xpath", f'{path1}tr[1]/td[4]/p/input').clear()
    driver.find_element("xpath", f'{path1}tr[1]/td[4]/p/input').send_keys(parse_fecha(fechaFin))
    driver.find_element("xpath", f'{path1}tr[2]/td[3]/input').click()

    # Obtengo las drogerias que puedo trazar
    time.sleep(1)
    drogerias = [i.text for i in Select(driver.find_element("xpath", f'{path1}tr[2]/td[2]/select')).options]
    
    # Agrego seccion de drogeria a la pestaña
    canvas2 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas2.config(background="#ECF0F1")
    canvas2.pack()

    # box text 3
    label3 = tk.Label(root, text='Seleccionar drogeria:')
    label3.config(font=('helvetica', 12), background="#F2F3F4")
    canvas2.create_window(200, 140, window=label3)

    # crear lista desplegable para seleccionar drogeria
    tipoDrog = ttk.Combobox(
        state = "readonly",
        values = drogerias
    )
    tipoDrog.config(width=40)
    canvas2.create_window(200, 165, window=tipoDrog)

    # boton para trazar
    button2 = tk.Button(text='Trazar', command=lambda:trazar(tipoDrog.get(), drogerias))
    button2.config(width=10, background="#D5D8DC")
    canvas2.create_window(200, 200, window=button2)
        
    
def parse_fecha(fecha_in):
    fecha = str(fecha_in)
    fsplit = fecha.split("-")
    return str(fsplit[2] + "/" + fsplit[1] + "/" + fsplit[0])


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

# box calendario inicio
label2 = tk.Label(root, text='Seleccionar fecha inicio:')
label2.config(font=('helvetica', 12), background="#F2F3F4")
canvas1.create_window(125, 90, window=label2)

calIn = DateEntry(root, date_pattern="dd/mm/yyyy")
calIn.pack()
canvas1.create_window(275, 90, window=calIn)

# box calendario fin
label2 = tk.Label(root, text='Seleccionar fecha final:')
label2.config(font=('helvetica', 12), background="#F2F3F4")
canvas1.create_window(125, 120, window=label2)

calFin = DateEntry(root, date_pattern="dd/mm/yyyy")
calFin.pack()
canvas1.create_window(275, 120, window=calFin)

# box text 4
label4 = tk.Label(root, text='Seleccionar forma:')
label4.config(font=('helvetica', 12), background="#F2F3F4")
canvas1.create_window(125, 150, window=label4)

# crear lista desplegable para seleccionar drogeria
forma = ttk.Combobox(
    state = "readonly",
    values = ["manual", "automatico"]
)
canvas1.create_window(275, 150, window=forma)

# boton para empezar trazar
button1 = tk.Button(text='Empezar trazar', command=main)
button1.config(width=10, background="#D5D8DC")
canvas1.create_window(200, 265, window=button1)

root.mainloop()

####################################################################
####################################################################
####################################################################
