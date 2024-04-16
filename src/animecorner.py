from requests_html import HTMLSession
import datetime
import json

session = HTMLSession()

start_time = datetime.datetime.now().timestamp()

print("Opening AnimeCorner")
r = session.get("https://animecorner.me/category/anime-corner/rankings/anime-of-the-week/")

print("Finding top chart")
new_url = r.html.find('div.content-list-right.content-list-center > div.header-list-style > h2 > a')[0].attrs['href']

print("Opening the top chart")
r = session.get(new_url)

ac_url = r.html.find("#penci-post-entry-inner > figure.wp-block-image.size-full > img")[0].attrs['src']
print(ac_url)

ac_time = datetime.datetime.now().timestamp()
ac_date = datetime.datetime.now().strftime("%d-%m-%Y")
print(f"Time taken: {ac_time - start_time}s")

with open("anime_images.json", "r") as f:
    data = json.load(f)

if not ac_date in data.keys():
    data[ac_date] = {
        "animecorner": {},
        "anitrendz": {}
    }

data[ac_date]["animecorner"] = {
    "image_url": ac_url,
    "last_updated_utc": int(ac_time)
}

with open("anime_images.json", "w") as f:
    json.dump(data, f, indent=4)

print("Written to file")


