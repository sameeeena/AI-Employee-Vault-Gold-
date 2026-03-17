"""
Facebook App Domain Fixer

Yeh script aapko Facebook App settings update karne mein help karegi.
"""

import webbrowser

# App configuration
APP_ID = "1275203508084665"

def main():
    print("=" * 70)
    print("  FACEBOOK APP DOMAIN FIX")
    print("=" * 70)
    print()
    print("⚠️  ERROR: App Domain configure nahi hai")
    print()
    print("📋 Solution - Step by Step:")
    print()
    print("=" * 70)
    print("  STEP 1: Facebook App Dashboard Open Karein")
    print("=" * 70)
    print()
    
    dashboard_url = f"https://developers.facebook.com/apps/{APP_ID}/settings/basic/"
    
    print(f"🔗 URL: {dashboard_url}")
    print()
    
    open_dash = input("Dashboard open karein? (y/n): ").strip().lower()
    if open_dash == 'y':
        webbrowser.open(dashboard_url)
    
    print()
    print("=" * 70)
    print("  STEP 2: App Domains Add Karein")
    print("=" * 70)
    print()
    print("Dashboard pe ye domains add karein:")
    print()
    print("   📝 App Domains field mein ye add karein:")
    print()
    print("      localhost")
    print("      facebook.com")
    print("      developers.facebook.com")
    print()
    print("   Ya agar aapke paas custom domain hai:")
    print("      yourdomain.com")
    print("      www.yourdomain.com")
    print()
    print("=" * 70)
    print("  STEP 3: Settings Save Karein")
    print("=" * 70)
    print()
    print("1. Neeche scroll karein")
    print("2. 'App Domains' field dhundhein")
    print("3. Comma-separated values daalein: localhost,facebook.com")
    print("4. Save Changes button click karein")
    print()
    print("=" * 70)
    print("  STEP 4: OAuth Redirect URI Add Karein")
    print("=" * 70)
    print()
    print("Facebook → Settings → Advanced:")
    print()
    print("   Valid OAuth Redirect URIs:")
    print("   https://developers.facebook.com/tools/explorer")
    print("   https://localhost")
    print("   http://localhost:8000")
    print()
    print("=" * 70)
    print("  ALTERNATIVE: Direct Token Link")
    print("=" * 70)
    print()
    print("Agar dashboard mein problem ho, toh direct link use karein:")
    print()
    
    # Direct OAuth link without redirect
    direct_link = f"https://www.facebook.com/v19.0/dialog/oauth?client_id={APP_ID}&scope=pages_manage_posts,pages_read_engagement,pages_show_list&response_type=token&display=page"
    
    print(f"🔗 {direct_link}")
    print()
    
    open_link = input("Direct link open karein? (y/n): ").strip().lower()
    if open_link == 'y':
        webbrowser.open(direct_link)
    
    print()
    print("=" * 70)
    print("  NEXT STEPS")
    print("=" * 70)
    print()
    print("1. Upar diye gaye steps follow karein")
    print("2. Domains save karne ke baad 5 minute wait karein")
    print("3. Phir se try karein: python get_facebook_token.py")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
