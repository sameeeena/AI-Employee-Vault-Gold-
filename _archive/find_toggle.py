"""Open Facebook App Settings - Where the toggle actually is"""
import webbrowser

app_id = "1275203508084665"

# Try different URLs where the toggle might be
urls = [
    f"https://developers.facebook.com/apps/{app_id}/review/",  # App Review page
    f"https://developers.facebook.com/apps/{app_id}/settings/basic/",  # Basic Settings
    f"https://developers.facebook.com/apps/{app_id}/app-review/",  # Alternative review page
]

print("Opening multiple Facebook pages...")
print()

for i, url in enumerate(urls, 1):
    print(f"{i}. {url}")
    webbrowser.open(url)

print()
print("Check your browser tabs!")
print()
print("Look for the toggle on ANY of these pages.")
