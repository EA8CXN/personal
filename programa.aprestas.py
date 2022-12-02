from watchdog.observers import Observer
from pathlib import Path
import telegram
import re
import json
import math




api_key = '5880151903:AAF3A5uFVjDMeqzi1LOfl2K6djomrE8LOdg'
user_id = '-558417283'
bot = telegram.Bot(token=api_key)
try:
    from watchdog.events import FileSystemEventHandler
    class MyEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            root = Path(event.src_path).name        
            file_name = Path(event.src_path).stem        
            extension = Path(event.src_path).suffix
            if extension == '.JPG':
                bot.send_message(chat_id=user_id, text=(('\U0001F4FB') + (' Nueva foto en el DMO La Matanza  ' )))
                bot.send_photo(chat_id=user_id, photo=open(event.src_path, 'rb'))
            if extension == '.json':
                fichero = open(event.src_path)
                with open (event.src_path, "r") as fichero1:
                    datos = fichero1.read()
                    datos = datos.replace("\n", ",")
                    datos = datos.replace("{,","\n{")
                    datos= datos.replace(",},", "}")
                jsondecoded=json.loads(datos)
                callsign = jsondecoded["callsign"]
                text= jsondecoded["text"]
                gps= jsondecoded["gps"]
                bot.send_message(chat_id=user_id, text=(('\U0001F4F2')+("\n") + (' Nuevo mensaje en el DMO La Matanza de: ' )+("\n")+ (callsign) +(":")+ ("\n")+(text)+("\n") + ('En posición GPS ') + (gps)))
                symbol_lat=(gps[:1]) # N or S
                latitude=(gps[1:4]) # degrees
                latitude_m=(gps[4:10]) #minutes raw
                latitude_m=int(latitude_m) / 10000 #minutes on decimal
                symbol_long=(gps[10:11]) # E or W
                longitude=(gps[11:14]) # degrees
                longitude_m=(gps[14:20]) #minutes rar
                longitude_m= int(longitude_m) / 10000 #minutes on decimal

                # Conversion to full degrees
                latitude_m=int(latitude_m) / 60
                latitude= int(latitude) + (latitude_m)
                if symbol_lat == "S":
                    latitude= latitude * (-1)

                longitude_m=int(longitude_m) / 60
                longitude = int(longitude) + (longitude_m)
                if symbol_long == "W":
                    longitude = longitude * (-1)


#                # Plot on a map
#                import plotly.graph_objects as go

#                mapbox_access_token = "pk.eyJ1IjoiZWE4Y3huIiwiYSI6ImNrenZ4OHRpOTAwa20yb2xudGFiOXV0ZnoifQ.39cAzs6-ABAvRu8YJDNuFw"
#                fig = go.Figure(go.Scattermapbox(
#                        lat=[(latitude)],
#                        lon=[(longitude)],
#                        mode='markers+text',
#                        marker=go.scattermapbox.Marker(size=14),
#                        text=[(callsign)], textposition = "bottom right",
#                    ))

#                fig.update_layout(
#                    #mapbox_style="dark",
#                    hovermode='closest',
#                    mapbox=dict(
#                        accesstoken=mapbox_access_token,
#                        bearing=0,
#                        center=go.layout.mapbox.Center(
#                            lat=28.3115,
#                            lon=-16.5662
#                        ),
#                        pitch=0,
#                        zoom=9
#                    )
#                )

#                fig.write_image('/tmp/news/fotos/msg.png')
#                bot.send_photo(chat_id=user_id, photo=open('/tmp/news/fotos/msg.png', 'rb'))


            
            
            
        
     
     
    observer = Observer()
    observer.schedule(MyEventHandler(), "/tmp/news", recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
except Exception:
    pass
