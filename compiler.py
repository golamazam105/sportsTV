import os
import requests
import re

# High-Performance Smart Dynamic APIs & Multi-Route Live Directories
M3U_SOURCES = [
    # BD Local & Global Toffee Engine Live Proxy
    "https://raw.githubusercontent.com/byte-capsule/Toffee-Channels-Link-Headers/main/toffee_channel_data.m3u",
    # Ultimate Auto-Refreshed Premium Playlists (Fancode, Willow, Sony, Star Inside)
    "https://raw.githubusercontent.com/swagapi/Premium-IPTV-Collection/main/sports_premium.m3u",
    "https://raw.githubusercontent.com/MohammadIPTV/IPTV-BGD/main/bangla.m3u",
    "https://raw.githubusercontent.com/ttoor5/Sports-IPTV/main/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

# Strict Multi-Variant Custom Matching Filters for Cricfy Standard Look
PREMIUM_CHANNELS_MAP = {
    # Willow Live Variants
    "willow": "Willow Cricket HD",
    "willow cricket": "Willow Cricket HD",
    "willowhd": "Willow Cricket HD",
    "willow xtra": "Willow Xtra HD",
    "willow usa": "Willow Cricket US",
    
    # FanCode App Live Variants
    "fancode": "FanCode Live",
    "fan code": "FanCode Live",
    "fancode 1": "FanCode 1 HD",
    "fancode 2": "FanCode 2 HD",
    "fancode 3": "FanCode 3 HD",
    
    # Premium Local & Sports OTT Networks
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
    "sports18 1": "Sports18 1 HD",
    "sports 18": "Sports18 HD",
    "ptv sports": "PTV Sports Live",
    "sky sports cricket": "Sky Sports Cricket HD",
    "sky sports main event": "Sky Sports Main Event",
    "astro supersport": "Astro SuperSport HD"
}

def clean_channel_name(title):
    title_lower = title.lower()
    # Broad regex parsing loop to catch every keyword dynamic instance
    for key, clean_name in PREMIUM_CHANNELS_MAP.items():
        if key in title_lower:
            return clean_name
    return None

def fetch_and_compile_streams():
    print("⚡ Activating Cricfy Ultra-Scraper V2 Engine...")
    compiled_data = {}
    
    for url in M3U_SOURCES:
        try:
            print(f"📡 Force scanning stream index source: {url}")
            response = requests.get(url, timeout=15)
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
                    
                    raw_title = line[comma_idx+1:].strip() if comma_idx != -1 else "Live Stream"
                    clean_name = clean_channel_name(raw_title)
                    
                    if clean_name:
                        current_meta['name'] = clean_name
                        current_meta['logo'] = logo_match.group(1) if logo_match else "https://i.imgur.com/Q5Z4y7T.png"
                        
                        # Set VIP category for FanCode, Willow and other main premium apps
                        name_lower = clean_name.lower()
                        if "willow" in name_lower or "fancode" in name_lower:
                            current_meta['category'] = "Premium OTT & Apps"
                        else:
                            current_meta['category'] = group_match.group(1) if group_match else "Live Sports"
                    else:
                        current_meta = None
                        
                elif line and not line.startswith('#') and current_meta:
                    stream_url = line
                    channel_name = current_meta['name']
                    
                    # Core Validation Check: Make sure URL is live stream protocol
                    if not stream_url.startswith('http'):
                        current_meta = None
                        continue
                    
                    if channel_name not in compiled_data:
                        compiled_data[channel_name] = {
                            "logo": current_meta['logo'],
                            "category": current_meta['category'],
                            "urls": []
                        }
                    
                    if stream_url not in compiled_data[channel_name]["urls"]:
                        compiled_data[channel_name]["urls"].append(stream_url)
                    current_meta = None
                    
        except Exception as e:
            print(f"⚠️ Source skipped info: {str(e)}")
            continue

    # Generate output
    m3u_output = "#EXTM3U\n"
    total_servers = 0
    
    for name, data in compiled_data.items():
        for index, url in enumerate(data["urls"]):
            server_label = f"Server {index + 1}"
            m3u_output += f'#EXTINF:-1 tvg-logo="{data["logo"]}" group-title="{data["category"]}", {name} ({server_label})\n'
            m3u_output += f'{url}\n\n'
            total_servers += 1
            
    with open("live_sports.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
        
    print(f"🎉 Compiled Done! {total_servers} Premium server links integrated safely.")

if __name__ == "__main__":
    fetch_and_compile_streams()
