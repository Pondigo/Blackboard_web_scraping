import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
# import requests
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)

def bb_login():
    driver.get("https://click.udlap.mx/webapps/login/")

bb_login()

#user_id

#Quita el pop-up de privacidad
driver.find_element_by_id("agree_button").click()

#Manda usuario y contraseña
driver.find_element_by_id("user_id").send_keys("ID")
driver.find_element_by_id("password").send_keys("PASSWORD")
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

#time.sleep(30)

iframeBB = driver.find_element_by_xpath("//*[@id='collabUltraLtiFrame']")
print(iframeBB)
driver.switch_to.frame(iframeBB)

wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='side-menu-toggle']"))).click()
#//*[@id="side-menu"]/div/nav/ul/li[3]/a
wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='side-menu']/div/nav/ul/li[3]/a"))).click()

#//*[@id="session-1b11e635c2aa4494977835c35a09c609-options-dropdown-toggle"]
#wait(driver, 10).until().click()
print(EC.presence_of_element_located((By.XPATH,"//*[contains(@id, 'options-dropdown-toggle')]")))
buttonsToSeeNow = driver.find_elements_by_xpath("//*[contains(@id, 'options-dropdown-toggle')]")


#button preserve focus-item loading-button      //*[@id="session-1b11e635c2aa4494977835c35a09c609-options-dropdown"]/ul/li/bb-loading-button/button

#presence_of_element_located
""" 
count = 0
for button in buttonsToSeeNow:
    count = count + 1
    button.click()
    html_collaborate = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html_collaborate, 'lxml')
    loadingButtons = soup.find_all('bb-loading-button')
    print('Botones encontrados:')
    print(len(loadingButtons))
    print('Loading buttons:')
    print(count)
    print(loadingButtons)
 """

#Busca la lista de los cursos

    #bb-loading-button
""" 
divMirarAhora = soup.find_all('button',class_="icon-button session-row-options list-item-icon has-tooltip ng-scope")
print(len(divMirarAhora))
for button in divMirarAhora:
    print('Button:')
    print(button.get('id'))
     """
#,class_="portletList-img courseListing coursefakeclass
#//*[@id="side-menu-toggle"]




#driver.find_element_by_id("side-menu-toggle").click()
""" #side-menu-toggle
try: #side-menu-toggle
    raise driver.find_element_by_xpath("//span[text()='Sala virtual'") 
except://*[@id="side-menu-toggle"]

    try:
        raise driver.find_element_by_xpath("//span[text()='Comunicación'")
    except:
        print('Sala virtual and comunicacion not exist')

#containerdiv
 """

""" 
while(currentCourses): {
    print(currentCourses),

    currentCourses.pop(-1)
}
   """  






""" 
html_login = requests.get('https://click.udlap.mx/webapps/login/')  
print(html_login)
soup = BeautifulSoup(html_login.text)
print(soup)

 """
""" 

soup = BeautifulSoup(html_login,'lxml')
with open('RecordBB1.html','r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content,'lxml')
    videoTag = soup.find('video').get('src')
    print(videoTag)    
"""
