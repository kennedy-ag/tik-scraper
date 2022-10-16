from TikTokApi import TikTokApi
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

VERIFY_FP="verify_l9abf09s_oAVqh1J1_Dtct_4pyU_950V_3Zq1M3iSAgwY"
X_PATH = f"/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/a"
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)


def extract(video_url: str, username: str, id: int):
    with TikTokApi(custom_verify_fp=VERIFY_FP) as api:
        video = api.video(url=video_url).bytes()
        video_info = api.video(url=video_url).as_dict

        video_info = {
            "views": video_info['stats']['playCount'],
            "likes": video_info['stats']['diggCount']
        }

        with open(f"./arquivos/{username}/videos/{username}__{id}.txt", 'w') as arq:
            arq.write(f"{video_info['views']}\n{video_info['likes']}")
        
        with open(f"./arquivos/{username}/videos/{username}__{id}.mp4", "wb") as out_file:
            out_file.write(video)
        
        get_comments(username, video_url, id)

def get_video_links_by_username(username: str):
    lista_de_links = []
    driver.get(f"https://www.tiktok.com/@{username}")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elementos = driver.find_elements(By.XPATH, X_PATH)
    for i in range(len(elementos)):
        lista_de_links.append(elementos[i].get_dom_attribute("href"))
    return lista_de_links

def close_driver():
    print("Fechando driver...")
    driver.close()
    print("Driver fechado.")

def create_profile_directory(username: str):
    os.mkdir(f'./arquivos/{username}')
    os.mkdir(f'./arquivos/{username}/videos')
    os.mkdir(f'./arquivos/{username}/comentarios')

def get_comments(username: str, url: str, video_id: int):
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    comentarios = [e.text for e in driver.find_elements(By.CLASS_NAME, "e1g2efjf6")]

    if len(comentarios) <=20:
        comentarios.extend(comentarios[0:15])

    for i in range(len(comentarios[0:40])):
        arq = open(f"./arquivos/{username}/comentarios/{username}__{video_id}__{i+1}.txt", 'w', encoding='utf8')
        arq.write(comentarios[i])
        arq.close()