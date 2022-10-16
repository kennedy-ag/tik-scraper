from funcoes import *
from datetime import datetime

inicial = datetime.now()
print(inicial.strftime("%H:%M:%S"))

username = "arianagrande"
video_id = 1

lista_de_videos = get_video_links_by_username(username)
if len(lista_de_videos)>=30:
    create_profile_directory(username)
    for i in range(len(lista_de_videos)):
        extract(lista_de_videos[i], username, video_id)
        video_id += 1

close_driver()

final = datetime.now()
print(final.strftime("%H:%M:%S"))
print(f"Tempo despendido: {final-inicial}")