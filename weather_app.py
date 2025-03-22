import tkinter as tk
from tkinter import ttk, messagebox
import requests
import io
from PIL import Image, ImageTk

API_KEY = "YOUR_API_KEY"
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast")
        self.root.geometry("400x400")

        self.create_widgets()
        self.load_icons()

    def load_icons(self):
        self.icons = {
            "01d": self.load_image("https://openweathermap.org/img/wn/01d@2x.png"),
            "01n": self.load_image("https://openweathermap.org/img/wn/01n@2x.png")
        }

    def load_image(self, url):
        response = requests.get(url, stream=True)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        return ImageTk.PhotoImage(image)
    
    def create_widgets(self):
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)

        self.city_entry = ttk.Entry(input_frame, width=25)
        self.city_entry.pack(side=tk.LEFT, expand=True)

        search_btn = ttk.Button(input_frame, text="Search", command=self.get_weather)
        search_btn.pack(side=tk.LEFT, padx=5)

        self.weather_frame = ttk.Frame(self.root, padding=20)
        self.weather_frame.pack(pady=10)

        self.icon_label = ttk.Label(self.weather_frame)
        self.icon_label.pack()

        self.temp_label = ttk.Label(self.weather_frame, font=('Helvetica', 24))
        self.temp_label.pack(pady=5)

        self.details_label = ttk.Label(self.weather_frame, wraplength=300)
        self.details_label.pack()

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Failed to fetch data: {str(e)}")
        except KeyError:
            messagebox.showerror("Data Error", "Invalid API response")

    def display_weather(self, data):
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        self.icon_label = ttk.Label(self.weather_frame)
        self.icon_label.pack()

        self.temp_label = ttk.Label(self.weather_frame, font=('Helvetica', 24))
        self.temp_label.pack(pady=5)

        self.details_label = ttk.Label(self.weather_frame, wraplength=300)
        self.details_label.pack()

        icon_code = data['weather'][0]['icon']
        icon_image = self.icons.get(icon_code, self.icons["01d"])
        self.icon_label.config(image=icon_image)
        self.icon_label.image = icon_image

        temp = data['main']['temp']
        self.temp_label.config(text=f"{temp}°C")

        details = [
            f"Weather: {data['weather'][0]['description']}",
            f"Humidity: {data['main']['humidity']}%",
            f"Wind Speed: {data['wind']['speed']} m/s",
            f"Pressure: {data['main']['pressure']} hPa"
        ]
        self.details_label.config(text="\n".join(details))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()