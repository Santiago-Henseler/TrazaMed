# import
import time
import sys
import tkinter as tk
from tkinter import messagebox

# abrimos el driver y establecemos parametros
from selenium import webdriver
driver = webdriver.Chrome("chromedriver.exe")

# recorremos el archivo txt y lo enviamos a la web
class Listado:
    def __init__(self, id, nComprobante, nAfil, nObra):
        self.id = id
        self.nComprobante = nComprobante
        self.nAfil = nAfil
        self.nObra = nObra

def clouser(txt, n):
    if n == 1:
        driver.close()
        messagebox.showerror(f"Error en la carga de datos", f"Datos erroneos en la traza: {txt}")
    elif n == 2:
        driver.close()
        driver.switch_to.window(handles[0])
        driver.close()
        messagebox.showerror(f"Error en la carga de datos", f"Datos erroneos en la traza: {txt}")
    else:
        driver.close()
        driver.switch_to.window(handles[0])
        driver.close()
        messagebox.showinfo("Proceso finalizado", txt)
    sys.exit()

with open("Escribir aca.txt") as file_object:
    leer = file_object.readlines()

# corroboramos que esten cargados los datos
Complet_list = []
if len(leer)<1:
    clouser("Faltan datos",1)
else:
    for i in leer:
        codes = i.split(" ")
        if (codes[3].strip() == "1" or codes[3].strip() == "2" or codes[3].strip() == "3") :
            constructor = Listado(codes[0], codes[1], codes[2], codes[3].strip())
            Complet_list.append(constructor)
        else:
            clouser(codes[0],1)

# entramos a la pagina y cargamos los datos
user = ***
clave = ***
path0 = '/html/body/form/table/tbody/tr'
driver.get("http://servicios.cofa.org.ar/ncr/")
driver.find_element("xpath", f'{path0}[1]/td[3]/select/option[9]').click()
driver.find_element("xpath", f'{path0}[2]/td[3]/input').send_keys(user)
driver.find_element("xpath", f'{path0}[3]/td[3]/input[1]').send_keys(clave)
driver.find_element("xpath", f'{path0}[3]/td[3]/input[2]').click()
driver.find_element("xpath",
                    '/html/body/form/div/table/tbody/tr/td/div[1]/table[2]/tbody/tr/td[1]/a').click()
handles = driver.window_handles
driver.switch_to.window(handles[1])
driver.find_element("xpath",
                    '/html/body/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/a[1]').click()

#entramos a la segunda pagina y iniciamos la traza
path1 = '/html/body/div[2]/table/tbody/tr/td/div/form/table/tbody/tr[2]/td/div[1]'
for i in Complet_list:
    driver.switch_to.parent_frame()
    driver.switch_to.default_content()
    driver.switch_to.window(handles[1])
    driver.find_element("xpath", f'{path1}/table[1]/tbody/tr/td[2]/input').send_keys(i.id)
    driver.find_element("xpath", f'{path1}/table[1]/tbody/tr/td[3]/input').click()
    exist = True
    try:
        driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[1]/td[2]/select/option[5]')
    except:
        exist = False
    if exist:
        # tipo comprobante
        driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[1]/td[2]/select/option[5]').click()
        driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[1]/td[6]/input').send_keys(i.nComprobante)
        # tipo de obra social
        obra = "0"
        if i.nObra == "1":
            # uom
            driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[2]/td[2]/select/option[222]').click()
            obra = "112103"
        elif i.nObra == "2":
            # ioma
            driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[2]/td[2]/select/option[81]').click()
            obra = "999977"
        else:
            # otras
            driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[2]/td[2]/select/option[545]').click()
            obra = "0"
        driver.find_element("xpath", f'{path1}/table[2]/tbody/tr[3]/td[2]/input').send_keys(i.nAfil)

        iframes = driver.execute_script('return document.getElementsByTagName("iframe"); ')

        for b in iframes:
            driver.switch_to.parent_frame()
            cTraza = b.get_attribute('src')
            nTraza = cTraza[51:58]
            driver.switch_to.frame(driver.find_element("xpath", f'{path1}/table[3]/tbody/tr[2]/td[6]/iframe'))
            time.sleep(1)
            driver.execute_script("""
                    var ventana =  window.open("http://datos.cofa.org.ar/trazabilidad/trazar32.asp?id=""" + nTraza + """&tc=R&fact=1&rto=""" + i.nComprobante + """&os=""" + obra + """&afi=""" + i.nAfil + """", "", "width=200,height=100"); 
                    setTimeout(function(){
                        ventana.close();
                        },5000);
               """)
            time.sleep(2)
        time.sleep(3)
    else:
        clouser(i.id, 2)

#cerramos la pagina y borramos los datos de la app
clouser("Todos los productos trazados", 3)
borrarTxt = open("Escribir aca.txt", "w")
borrarTxt.write("")
borrarTxt.close()
webdriver.Chrome("chromedriver.exe").close()
