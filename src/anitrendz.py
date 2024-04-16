from requests_html import HTMLSession
import json
import datetime

start_time = datetime.datetime.now().timestamp()

session = HTMLSession()

print("Opening Anitrendz")
r = session.get("https://www.anitrendz.com/")
print("Rendering webpage...")
r.html.render(scrolldown=True, sleep=0.5, timeout=10)
img = r.html.find('#simple-tabpanel-0 > div > a > img')

img_url = f"https://www.anitrendz.com{img[0].attrs['src']}"
print(img_url)


now = datetime.datetime.now()
at_date = now.strftime("%d-%m-%Y")
at_timestamp = now.timestamp()

print(f"Time taken: {at_timestamp - start_time}s")

with open("anime_images.json", "r") as f:
    data = json.load(f)

if not at_date in data.keys():
    data[at_date] = {
        "animecorner": {},
        "anitrendz": {}
    }

data[at_date]["anitrendz"] = {
    "image_url": img_url,
    "last_updated_utc": int(at_timestamp)
}

with open("anime_images.json", "w") as f:
    json.dump(data, f, indent=4)

print("Written to file")