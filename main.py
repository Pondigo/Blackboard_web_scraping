import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import requests
import os
import errno

file = open("./Personal-Data.txt", "r") # "r" reading file
user_data = file.read().split('\n')

# import requests
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)

# Function to open login
def bb_login():
    driver.get("https://click.udlap.mx/webapps/login/")

bb_login()

#user_id

#Quita el pop-up de privacidad
driver.find_element_by_id("agree_button").click()

#Manda usuario y contraseña
driver.find_element_by_id("user_id").send_keys(user_data[0])
driver.find_element_by_id("password").send_keys(user_data[1])
driver.find_element_by_id("entry-login").click()

#Lee todos los cursos
time.sleep(2)

#Obtiene el HTML
html_login = driver.execute_script("return document.body.innerHTML;")
soup = BeautifulSoup(html_login, 'lxml')

#Busca la lista de los cursos
containerCourses = soup.find_all('ul',class_="portletList-img courseListing coursefakeclass")

#Guarda los nombres de los cursos
currentCourses = []
for ultag in containerCourses:
    for litag in ultag.find_all('li'):
        tempTextLinked = litag.find('a').get_text()
        currentCourses.append(tempTextLinked)



#Empieza por el ultimo curso
driver.find_element_by_link_text(currentCourses[-1]).click()
#Define la ruta correspondiente a este curso
currentDir = str(currentCourses[-1]).replace(':','_')

#Define la ruta de la carpeta o la crea si no existe
try:
    os.mkdir(currentDir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
#Espera a que cargue
time.sleep(2)

#Entra a SalaVirtual
try:
    wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Sala virtual')]"))).click()
except:
    try:
        wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Comunicación')]"))).click()
    except:
        print('Erroooor')

#Entra a Blackboard Collaborate Ultra
time.sleep(1)
wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Blackboard Collaborate Ultra')]"))).click()

#Entra al iFrame
iframeBB = driver.find_element_by_xpath("//*[@id='collabUltraLtiFrame']")
driver.switch_to.frame(iframeBB)
time.sleep(10)
#Abre menu deslizable para seleccionar grabaciones/sesiones
wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='side-menu-toggle']"))).click()
#Selecciona grabaciones
wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='side-menu']/div/nav/ul/li[3]/a"))).click()
#Da click en un boton de opcion de grabacion, para que se hagan visibles los demas.
wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'options-dropdown-toggle')]"))).click()

tabsOnChrome = []
nameOfTabsOnChrome = []

tabsOnChrome.append(driver.current_window_handle)
nameTab = 'CTab recordings of: ' + str(currentCourses[-1])
nameOfTabsOnChrome.append(nameTab)

##Busacar boton para mirar ahora con beautifulsoup, debido a que puede tambien estar definido para obtener el enlace 
#Esta funcion retorna los botones del div que hizo visible el ultimo click
def getCSSSelectorGrabationViewChargeButtons():
    html_login = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html_login, 'lxml')
    trs = soup.find_all('div',class_="dropdown-pane ng-scope ng-isolate-scope is-open")
    returnButtons = []
    for tr in trs:
        buttons = tr.find_all('button')
        for button in buttons:
            ariaLabelofCurrentButton = button.get('aria-label')
            tempCSSSelector = "button"+ "[aria-label='" + str(ariaLabelofCurrentButton) + "']"
            returnButtons.append(tempCSSSelector)
    return returnButtons

def openRecording(btcav):
    try:
        wait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btcav[1]))).click()
        wait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btcav[0]))).click()
        cTabsOnChrome = driver.window_handles
        #Buscar en el arreglo las ya existentes
        for aExistentTabs in tabsOnChrome:
            cTabsOnChrome.pop(cTabsOnChrome.index(aExistentTabs))
        if(len(cTabsOnChrome) == 1):
            tabsOnChrome.append(cTabsOnChrome[0])
            nameTab = selectorToNameVideo(btcav[0])
            nameOfTabsOnChrome.append(nameTab)
        else:
            print('[ERROR] Las ventanas sobrantes son: ' + str(tabsOnChrome) + '\n\tCon una logitid de: ' + str(len(tabsOnChrome)))
    except:
        try:
            wait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btcav[0]))).click()
            cTabsOnChrome = driver.window_handles
            #Buscar en el arreglo las ya existentes
            for aExistentTabs in cTabsOnChrome:
                cTabsOnChrome = tabsOnChrome.pop(tabsOnChrome.index(aExistentTabs))
            if(len(cTabsOnChrome) == 1):
                tabsOnChrome.append(cTabsOnChrome[0])
                nameTab = selectorToNameVideo(btcav[0])
                nameOfTabsOnChrome.append(nameTab)
            else:
                print('[ERROR] Las ventanas sobrantes son: ' + str(tabsOnChrome) + '\n\tCon una logitid de: ' + str(len(tabsOnChrome)))
                
        except: 
            print('No se pudo dar click a ningún boton.')
    finally:
        print('Se accedio exitosamente a la grabación')

def downloadVideoFromPRO(tabToVideo,name,dir):
    driver.switch_to_window(tabToVideo)
    html = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html, 'lxml')
    videoSrc = soup.find('video').get('src')
    name= str(name) + ".mp4"
    r=requests.get(videoSrc, timeout=30, stream=True)
    print ('Conectado para descargar: ' + str(name))
    completeName = os.path.join(str(dir), name)
    f=open(completeName,'wb')
    print ("Descargando: " + str(name))
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print ("Se ha completado la descarga de: " + str(name))
    f.close()
    driver.switch_to_window(driver.window_handles[0])

def selectorToNameVideo(cssSelectorMirarAhora):
    tempName = cssSelectorMirarAhora.split(':')
    tempName = tempName[1].split(' a las')
    tempName = tempName[0].replace('/','_')
    tempName = tempName.lstrip()
    return tempName

bfr = getCSSSelectorGrabationViewChargeButtons()

openRecording(bfr)

#Encuentra los botones de opcion de grabación
buttonsToSeeNow = driver.find_elements_by_xpath("//*[contains(@id, 'options-dropdown-toggle')]")


""" 
tabs = driver.window_handles
cTabIndex = tabs.index(driver.current_window_handle)
tabs.pop(cTabIndex)
#borrar los ya registrados

downloadVideoFromPRO(tabs[0],selectorToNameVideo(bfr[0]),currentCourses[-1])

""" 
buttonsToSeeNow.pop(0)

#Da click en todos los botones de opcion de grabación
for button in buttonsToSeeNow:
    button.click()
    bgvc = getCSSSelectorGrabationViewChargeButtons()
    openRecording(bgvc)

print('Las ventanas registradas son: \t' + str(tabsOnChrome))
print('Y corresponden a:             \t' + str(nameOfTabsOnChrome))

time.sleep(60*2)
if(len(tabsOnChrome) == len(nameOfTabsOnChrome)):
    currentRecord = 0
    for nameRecording in nameOfTabsOnChrome:
        if(str(nameRecording).split(':')[0] != 'CTab recordings of'):
            print('Ha descargar ' + str(nameRecording) + '!')
            downloadVideoFromPRO(tabsOnChrome[currentRecord],nameRecording,currentDir)
        else:
            print('Es la pagina principal, no se descarga nada de aqui')
        currentRecord = currentRecord + 1
else:
    print('Error al registrar las paginas y sus nomnbres')
    
    

""" 
while(currentCourses): {
    print(currentCourses),

    #Ejecutar script principal

    

    #Retornar a listado de cursos 
    currentCourses.pop(-1)
}
"""  


""" 
#Sirve para encontrar la fuente del video
soup = BeautifulSoup(html_login,'lxml')
with open('RecordBB1.html','r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content,'lxml')
    videoTag = soup.find('video').get('src')
    print(videoTag)    
"""
