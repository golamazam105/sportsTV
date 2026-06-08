import os
import requests
import re

# Premium Dynamic IPTV APIs & Multi-Variant Sports Repositories
M3U_SOURCES = [
    # Top Premium Sources for Willow, FanCode, and OTT Platforms (Auto-Token Refreshed)
    "https://raw.githubusercontent.com/byte-capsule/Toffee-Channels-Link-Headers/main/toffee_channel_data.m3u",
    "https://raw.githubusercontent.com/swagapi/Premium-IPTV-Collection/main/sports_premium.m3u",
    "https://raw.githubusercontent.com/YousefAlZhrany/IPTV/main/Sport.m3u",
    "https://raw.githubusercontent.com/MohammadIPTV/IPTV-BGD/main/bangla.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

# Advanced Strict Mapping Table for Willow, FanCode & Ultimate Premium OTT Variants
PREMIUM_CHANNELS_MAP = {
    # Willow Cricket Variants
    "willow cricket": "Willow Cricket HD",
    "willow hd": "Willow Cricket HD",
    "willow xtra": "Willow Xtra HD",
    "willowusa": "Willow Cricket US",
    
    # FanCode Variants
    "fancode": "FanCode Live",
    "fan code": "FanCode Live",
    "fancode 1": "FanCode 1 HD",
    "fancode 2": "FanCode 2 HD",
    "fancode 3": "FanCode 3 HD",
    
    # Core Sports OTT & Premium Channels
    "t sports": "T Sports HD",
    "tsports": "T Sports HD",
    "gazi tv": "GTV (Gazi TV)",
    "gtv": "GTV (Gazi TV)",
    "star sports 1 hd": "Star Sports 1 HD",
    "star sports 1 hindi": "Star Sports 1 Hindi",
    "star sports select 1": "Star Sports Select 1",
    "star sports select 2": "Star Sports Select 2",
    "sony sports ten 1": "Sony Sports Ten 1 HD",
    "sony sports ten 2": "Sony Sports Ten 2 HD",
    "sony sports ten 3": "Sony Sports Ten 3 HD",
    "sony sports ten 5": "Sony Sports Ten 5 HD",
    "sports18 1 hd": "Sports18 1 HD",
    "sports18 k发展": "Sports18 1 HD",
    "sports 18": "Sports18 HD",
    "ptv sports": "PTV Sports Live",
    "sky sports cricket": "Sky Sports Cricket HD",
    "sky sports main event": "Sky Sports Main Event",
    "astro supersport": "Astro SuperSport HD"
}

def clean_channel_name(title):
    title_lower = title.lower()
    # Check for specific premium variants first
    for key, clean_name in PREMIUM_CHANNELS_MAP.items():
        if key in title_lower:
            return clean_name
    return None

def fetch_and_compile_streams():
    print("⚡ Starting Cricfy Ultra-Scraper Engine with Premium OTT Support...")
    compiled_data = {}
    
    for url in M3U_SOURCES:
        try:
            print(f"📡 Deep scanning source for Premium OTTs: {url}")
            response = requests.get(url, timeout=12)
            if response.status_code != 200:
                continue
                
            lines = response.text.split('\n')
            current_meta = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    current_meta = {}
                    logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                    group_match = re.search(r'group-title="([^"]+)"', line)
                    comma_idx = line.rfind(',')
                    
                    raw_title = line[comma_idx+1:].strip() if comma_idx != -1 else "Premium Match"
                    clean_name = clean_channel_name(raw_title)
                    
                    if clean_name:
                        current_meta['name'] = clean_name
                        current_meta['logo'] = logo_match.group(1) if logo_match else "https://i.imgur.com/Q5Z4y7T.png"
                        current_meta['category'] = "Premium OTT & Sports" if "willow" in clean_name.lower() or "fancode" in clean_name.lower() else (group_match.group(1) if group_match else "Live Sports")
                    else:
                        current_meta = None
                elif line and not line.startswith('#') and current_meta:
                    stream_url = line
                    channel_name = current_meta['name']
                    
                    if channel_name not in compiled_data:
                        compiled_data[channel_name] = {
                            "logo": current_meta['logo'],
                            "category": current_meta['category'],
                            "urls": []
                        }
                    
                    # Store multiple servers/variants safely
                    if stream_url not in compiled_data[channel_name]["urls"]:
                        compiled_data[channel_name]["urls"].append(stream_url)
                    current_meta = None
                    
        except Exception as e:
            print(f"⚠️ Source skip info: {str(e)}")
            continue

    # Generate the Ultimate Cricfy-Standard M3U
    m3u_output = "#EXTM3U\n"
    total_nodes = 0
    
    for name, data in compiled_data.items():
        for index, url in enumerate(data["urls"]):
            server_label = f"Server {index + 1}"
            m3u_output += f'#EXTINF:-1 tvg-logo="{data["logo"]}" group-title="{data["category"]}", {name} ({server_label})\n'
            m3u_output += f'{url}\n\n'
            total_nodes += 1
            
    with open("live_sports.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
        
    print(f"🎉 Engine compiled successfully! Deployed {total_nodes} Premium Nodes into production.")

if __name__ == "__main__":
    fetch_and_compile_streams()
