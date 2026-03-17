"""Open Facebook Permission Link"""
import webbrowser

url = "https://www.facebook.com/v19.0/dialog/oauth?client_id=1275203508084665&scope=pages_manage_posts,pages_read_engagement,pages_show_list,instagram_basic,instagram_content_publish&response_type=token&display=page"

print("Opening Facebook Permission page...")
print(f"URL: {url}")
webbrowser.open(url)
print("Done! Check your browser.")
