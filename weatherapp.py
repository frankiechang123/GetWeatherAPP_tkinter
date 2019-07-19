import tkinter as tk
import requests
import datetime


root=tk.Tk()

window=tk.Canvas(root,width=400,height=400)
window.pack()
bg_image=tk.PhotoImage(file="Bg.png")
bg_label=tk.Label(root, image=bg_image)

frame1=tk.Frame(root,bg="#42f4e5",bd=5)
frame2=tk.Frame(root,bg="#42f4e5",bd=5)
button=tk.Button(frame1,text="Get Weather",command=lambda:getWeather(entry.get()))
entry=tk.Entry(frame1,font=12)
label=tk.Label(frame2,anchor="nw",justify="left",font=12,text="Please enter a city.")

final_text="yes"


def getWeather(text):
    try:
        url="http://api.openweathermap.org/data/2.5/weather"
        key= "5d8684beff6068a09c790dfc8020dfe6"
        params={"APPID":key,"q":text,"units":"metric"}
        response= requests.get(url,params=params)
        weather_json=response.json()
        print(weather_json)
        cityName=weather_json["name"]
        Temperature="%s---%s" %(weather_json["main"]["temp_min"],weather_json["main"]["temp_max"])
        desc=weather_json["weather"][0]["description"]
        sunrise_time=datetime.datetime.fromtimestamp(weather_json["sys"]["sunrise"]) #sunrise_time in computer time
        sunset_time=datetime.datetime.fromtimestamp(weather_json["sys"]["sunset"])  #sunset_time in computer time
        utctime=datetime.datetime.utcnow()  #utc time
       
        hour_difference=datetime.timedelta(hours=datetime.datetime.now().hour-utctime.hour-weather_json["timezone"]/3600) 
        sunrise_time_str=(sunrise_time-hour_difference).time() #converting timezone (could make another function)
        sunset_time_str=(sunset_time-hour_difference).time()
            
        local_time=(datetime.timedelta(hours=weather_json["timezone"]/3600)+utctime).replace(microsecond=0)
        print(utctime.hour+weather_json["timezone"]/3600)
        final_text="City Name: %s\nTemperature: %s(Celsius)\nWeather: %s\nSunrise: %s\nSunset: %s\nLocal Time: %s" % (cityName,Temperature,desc,sunrise_time_str,sunset_time_str,local_time)
        
    except: #send error messages
        message_text=weather_json["message"]
        final_text="An error has occured\n%s" %(message_text) 
        
    label["text"]=final_text 
    

bg_label.place(relwidth=1,relheight=1)
frame1.place(relx=0.5,rely=0.1,relwidth=0.9,relheight=0.1,anchor="n")
frame2.place(relx=0.5,rely=0.25,relwidth=0.9,relheight=0.65,anchor="n")
button.place(relx=0.7,relwidth=0.3,relheight=1)
entry.place(relwidth=0.6,relheight=1)
label.place(relwidth=1,relheight=1)

root.mainloop()