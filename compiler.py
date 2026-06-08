import os
import requests

# আপনার নতুন এবং সঠিক গুগল অ্যাপস স্ক্রিপ্ট ওয়েব অ্যাপ ইউআরএল
GSHEET_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz3KXlxSlNtsOYc5OLELIChSSI1TXyCfxGgzmx8ndlN4aY50dunSWG0eELK_WifXsixdg/exec"

def generate_sports_m3u():
    print("📡 Fetching live data from your new Google Sheet Web App...")
    try:
        # গুগল শিট ওয়েব অ্যাপ থেকে রিয়েল-টাইম ডাটা ফেচ করা
        response = requests.get(GSHEET_WEB_APP_URL, timeout=15)
        if response.status_code != 200:
            print("❌ Failed to fetch data. Please check Web App permission (Must be set to 'Anyone').")
            return
        
        data = response.json()
        
        m3u_content = "#EXTM3U\n"
        channels_processed = 0
        
        for item in data:
            name = item.get("name", "Premium Sports")
            url = item.get("url", "").strip()
            logo = item.get("logo", "https://i.imgur.com/Q5Z4y7T.png")
            category = item.get("category", "Live Sports")
            server = item.get("server", "Server 1")
            
            if not url:
                continue
                
            # ক্রিকফাই স্টাইল গ্রুপিং করার জন্য চ্যানেলের নামের সাথে সার্ভার আইডি ট্যাগিং
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}", {name} ({server})\n'
            m3u_content += f'{url}\n\n'
            channels_processed += 1
            
        # গিটহাব ওয়ার্কস্পেসে M3U ফাইলটি রাইট করা
        with open("live_sports.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"🎉 Success! Generated live_sports.m3u with {channels_processed} live server streams!")
        
    except Exception as e:
        print(f"❌ Error during compilation: {str(e)}")

if __name__ == "__main__":
    generate_sports_m3u()
