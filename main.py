import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

file = open("./Personal-Data.txt", "r") # "r" reading file
user_data = file.read().split('\n')

# import requests
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
# 
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

#Primer curso

#Empieza por el ultimp curso
driver.find_element_by_link_text(currentCourses[-1]).click()
#Espera a que cargue
time.sleep(2)
#Entra a SalaVirtual
wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Sala virtual')]"))).click()
#Entra a Blackboard Collaborate Ultra
time.sleep(1)
wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Blackboard Collaborate Ultra')]"))).click()

iframeBB = driver.find_element_by_xpath("//*[@id='collabUltraLtiFrame']")
print(iframeBB)
driver.switch_to.frame(iframeBB)

wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='side-menu-toggle']"))).click()

wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='side-menu']/div/nav/ul/li[3]/a"))).click()


print(EC.presence_of_element_located((By.XPATH,"//*[contains(@id, 'options-dropdown-toggle')]")))
buttonsToSeeNow = driver.find_elements_by_xpath("//*[contains(@id, 'options-dropdown-toggle')]")

#Da click en todos los botones de opcion de grabación
for button in buttonsToSeeNow:
    button.click()



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
