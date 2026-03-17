"""Open Facebook App Review & Permission pages directly"""
import webbrowser

app_id = "1275203508084665"

# Direct URLs to try
urls = [
    # App Review - Permissions
    f"https://developers.facebook.com/apps/{app_id}/app-review/permissions/",
    
    # Facebook Login settings
    f"https://developers.facebook.com/apps/{app_id}/fb-login/",
    
    # App Review submission
    f"https://developers.facebook.com/apps/{app_id}/app-review/submissions/",
    
    # Graph API Explorer with your app
    f"https://developers.facebook.com/tools/explorer/{app_id}/",
]

print("Opening Facebook pages...")
print()

for i, url in enumerate(urls, 1):
    print(f"{i}. {url}")
    webbrowser.open(url)

print()
print("Check your browser tabs!")
print()
print("Look at tabs 1-3 for permission status.")
print("Tab 4 is Graph API Explorer to get token.")
