"""Open Facebook App Dashboard"""
import webbrowser

# Open the app dashboard directly
app_id = "1275203508084665"
url = f"https://developers.facebook.com/apps/{app_id}/dashboard/"

print(f"Opening your App Dashboard...")
print(f"App ID: {app_id}")
print(f"URL: {url}")
webbrowser.open(url)
print("Done! Check your browser.")
