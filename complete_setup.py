"""
COMPLETE FACEBOOK DEVELOPER SETUP GUIDE
========================================

This will open all required pages. Follow along!
"""
import webbrowser

print("=" * 80)
print("  COMPLETE FACEBOOK DEVELOPER SETUP")
print("=" * 80)
print()

# Open all required pages
urls = [
    ("1. Facebook Developer Registration", "https://developers.facebook.com/"),
    ("2. Facebook Business", "https://business.facebook.com/"),
]

print("Opening required pages...")
for name, url in urls:
    print(f"  {name}")
    webbrowser.open(url)

print()
print("Now follow the step-by-step guide below!")
print()
print("=" * 80)
