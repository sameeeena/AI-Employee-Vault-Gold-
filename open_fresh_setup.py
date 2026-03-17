"""Open all Facebook pages for fresh setup"""
import webbrowser

urls = [
    ("1. Facebook Login", "https://www.facebook.com/"),
    ("2. Create App", "https://developers.facebook.com/apps/"),
    ("3. Graph API Explorer", "https://developers.facebook.com/tools/explorer/"),
]

print("Opening Facebook pages for fresh setup...")
print()

for name, url in urls:
    print(f"  {name}: {url}")
    webbrowser.open(url)

print()
print("Follow the guide in: fresh_facebook_setup.py")
print("Or see: FRESH_SETUP_GUIDE.md")
