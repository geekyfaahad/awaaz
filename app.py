# aiohttp+uvloop

# from flask import Flask, render_template, request
# from cryptography.fernet import Fernet
# import aiohttp
# import asyncio
# import uvloop  # Import uvloop
# from bs4 import BeautifulSoup
# from flask_compress import Compress

# # Set uvloop as the default event loop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# app = Flask(__name__)
# Compress(app)

# # Function to map user input to time ranges
# def get_time_range(user_choice):
#     time_ranges = {
#         "rf": "h,sbd:1",  # Recent news (last hour)
#         "dn": "d",  # News from the past day
#         "wn": "w",  # News from the past week
#         "mn": "m",  # News from the past month
#         "yn": "y",  # News from the past year
#     }
#     return time_ranges.get(user_choice, "")
# def load_key():
#     with open("encryption_key.key", "rb") as key_file:
#         return key_file.read()

# def decrypt_url(encrypted_url, key):
#     cipher = Fernet(key)
#     decrypted_url = cipher.decrypt(encrypted_url).decode()
#     return decrypted_url

# async def fetch_news(time_range):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
#     }

#     # Load and decrypt the URL
#     key = load_key()
#     encrypted_url = b"gAAAAABnUiY7dXeOo3kEn8vE799th4up_op1WETMRump6p3LvA4PVJxOrhDMqd0jF7bwmZiIHX_XYY2ZqUt5AlvfYr7VHrfykiW1JpjYfNiGG8EneZJRqvvvDqJTMdNgbxD_3bTR-Ax2h3JAHlauoLyBtsvh_g5i9uwrxTgZWpUNjEKWPApMbeZhOvpJrg37L-bmBfbvlosyfOEDX3JrFs3PzG_eRHIWt_X9N9o0OgPkYyNq5a5dyZU1pD0OyaiYQAdo7IHZJRaHGUuy0oBjdvR-2hifOtI2QHgWAhvhkf2xXTGmv_Q9wF8rAcke5joJFGHmB5g-JyHVknE17e8juRITfTribariOBn7uGZ4zpzAmKk_jB3xaL5jgxJHuVghxpmQ4-dVDSaeCXrDNvjNj2grUXLq1mCew5SH2ARCxg_xt938277OrxDjZ2ox4f3XDMW6Umpp5Bzfk50D_ixQR33tBXegj2NWsvb-f17Nv3q1_XbvPzNqM_Luu9U57ITM1IrfzIxi1SFbrjMSUZqFiOAtYWyqX-4X3QUnQxZ_CcDD-yT4PASGc14SBj-GGhU1Zz3p3XIjnoDvQYOI6gVq1t5LPDvsUEEurbvdrBE7aETZaRNCzQwKdeqBtmrfDlKIoGCkBBaVAYlNo5CGcu1nU-HxM2UtK1HF_g=="
#     decrypted_url = decrypt_url(encrypted_url, key)
#     url = decrypted_url.format(time_range=time_range)
#     print(url)

#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.get(url, headers=headers, timeout=10) as response:
#                 if response.status != 200:
#                     return []

#                 html_content = await response.text()
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 news_items = soup.find_all('div', class_='SoAPf')
#                 excluded_keywords = [
#                     "Greater Kashmir",
#                     "Page 1 Archives",
#                     "National Archives",
#                     "Kashmir Latest News Archives",
#                 ]

#                 results = []
#                 for item in news_items:
#                     headline = item.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d')
#                     headline_text = headline.text.strip() if headline else "No headline available"
#                     if any(keyword in headline_text for keyword in excluded_keywords):
#                         continue

#                     summary = item.find('div', class_='GI74Re nDgy9d')
#                     summary_text = summary.text.strip() if summary else "No summary available"

#                     time = item.find('div', class_='OSrXXb rbYSKb LfVVr')
#                     time_text = time.text.strip() if time else "No time information"

#                     link_tag = item.find_parent('a', class_='WlydOe')
#                     link = link_tag['href'] if link_tag else "No link available"

#                     results.append(
#                         {
#                             "headline": headline_text,
#                             "summary": summary_text,
#                             "time": time_text,
#                             "link": link,
#                         }
#                     )

#                 return results
#         except aiohttp.ClientError as e:
#             print(f"HTTP error occurred: {e}")
#             return []
#         except asyncio.TimeoutError:
#             print("Request timed out.")
#             return []

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/results', methods=['POST'])
# def results():
#     user_choice = request.form.get('filter')
#     time_range = get_time_range(user_choice)
#     # Run the async function using asyncio.run()
#     news_data = asyncio.run(fetch_news(time_range))
#     return render_template('results.html', news_data=news_data)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)




# requests method


# from flask import Flask, render_template, request
# from cryptography.fernet import Fernet
# import requests
# from bs4 import BeautifulSoup
# from flask_compress import Compress
# app = Flask(__name__)
# Compress(app)
# # Function to map user input to time ranges
# def get_time_range(user_choice):
#     time_ranges = {
#         "rf": f'{"h"}{",sbd:1"}',        # Recent news (last hour)
#         "dn": "d",       # News from the past day
#         "wn": "w",       # News from the past week
#         "mn": "m",       # News from the past month
#         "yn": "y"        # News from the past year
#     }
#     return time_ranges.get(user_choice, "")

# def load_key():
#     with open("encryption_key.key", "rb") as key_file:
#         return key_file.read()

# def decrypt_url(encrypted_url, key):
#     cipher = Fernet(key)
#     decrypted_url = cipher.decrypt(encrypted_url).decode()
#     return decrypted_url


# def fetch_news(time_range):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
#     }
#     key = load_key()
#     encrypted_url = b"gAAAAABnUiY7dXeOo3kEn8vE799th4up_op1WETMRump6p3LvA4PVJxOrhDMqd0jF7bwmZiIHX_XYY2ZqUt5AlvfYr7VHrfykiW1JpjYfNiGG8EneZJRqvvvDqJTMdNgbxD_3bTR-Ax2h3JAHlauoLyBtsvh_g5i9uwrxTgZWpUNjEKWPApMbeZhOvpJrg37L-bmBfbvlosyfOEDX3JrFs3PzG_eRHIWt_X9N9o0OgPkYyNq5a5dyZU1pD0OyaiYQAdo7IHZJRaHGUuy0oBjdvR-2hifOtI2QHgWAhvhkf2xXTGmv_Q9wF8rAcke5joJFGHmB5g-JyHVknE17e8juRITfTribariOBn7uGZ4zpzAmKk_jB3xaL5jgxJHuVghxpmQ4-dVDSaeCXrDNvjNj2grUXLq1mCew5SH2ARCxg_xt938277OrxDjZ2ox4f3XDMW6Umpp5Bzfk50D_ixQR33tBXegj2NWsvb-f17Nv3q1_XbvPzNqM_Luu9U57ITM1IrfzIxi1SFbrjMSUZqFiOAtYWyqX-4X3QUnQxZ_CcDD-yT4PASGc14SBj-GGhU1Zz3p3XIjnoDvQYOI6gVq1t5LPDvsUEEurbvdrBE7aETZaRNCzQwKdeqBtmrfDlKIoGCkBBaVAYlNo5CGcu1nU-HxM2UtK1HF_g=="
#     decrypted_url = decrypt_url(encrypted_url, key)
#     time_range = time_range  # Example: Replace with "d7" for the last 7 days
#     url = decrypted_url.format(time_range=time_range)
#     print(url)
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return []


#     soup = BeautifulSoup(response.text, 'html.parser')
#     news_items = soup.find_all('div', class_='SoAPf')
#     excluded_keywords = ["Greater Kashmir", "Page 1 Archives", "National Archives"]

#     results = []
#     for item in news_items:
#         headline = item.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d')
#         headline_text = headline.text.strip() if headline else "No headline available"
#         if any(keyword in headline_text for keyword in excluded_keywords):
#             continue

#         summary = item.find('div', class_='GI74Re nDgy9d')
#         summary_text = summary.text.strip() if summary else "No summary available"

#         time = item.find('div', class_='OSrXXb rbYSKb LfVVr')
#         time_text = time.text.strip() if time else "No time information"

#         link_tag = item.find_parent('a', class_='WlydOe')
#         link = link_tag['href'] if link_tag else "No link available"

#         results.append({
#             "headline": headline_text,
#             "summary": summary_text,
#             "time": time_text,
#             "link": link,
#         })

#     return results

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/results', methods=['POST'])
# def results():
#     user_choice = request.form.get('filter')
#     time_range = get_time_range(user_choice)
#     news_data = fetch_news(time_range)
#     return render_template('results.html', news_data=news_data)

# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0',port=5000)





# aiohttp code


from flask import Flask, render_template, request, jsonify, send_from_directory
from cryptography.fernet import Fernet
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from flask_compress import Compress
import logging
from threading import Thread, Lock
import time
from collections import defaultdict
from datetime import datetime, timedelta
import atexit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
Compress(app)

rate_limit = 20
rate_limit_window = 43200  # 12 hours in seconds
request_counts = defaultdict(lambda: {"count": 0, "reset_time": datetime.now()})
lock = Lock()

def get_client_ip():
    """Retrieve the IP address of the client."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def is_rate_limited(ip):
    now = datetime.now()
    with lock:
        if now >= request_counts[ip]["reset_time"]:
            request_counts[ip]["count"] = 1  # Reset count with current request
            request_counts[ip]["reset_time"] = now + timedelta(seconds=rate_limit_window)
            return False
        else:
            request_counts[ip]["count"] += 1
            if request_counts[ip]["count"] > rate_limit:
                return True
        return False

def cleanup_request_counts():
    now = datetime.now()
    to_remove = [ip for ip, data in request_counts.items() if now >= data["reset_time"] and data["count"] == 0]
    for ip in to_remove:
        del request_counts[ip]

def start_cleanup():
    while True:
        cleanup_request_counts()
        time.sleep(3600)  # Clean up every hour

cleanup_thread = Thread(target=start_cleanup)
cleanup_thread.daemon = True
cleanup_thread.start()

atexit.register(cleanup_request_counts)

def get_time_range(user_choice):
    time_ranges = {
        "rf": "h,sbd:1",  # Recent news (last hour)
        "dn": "d",  # News from the past day
        "wn": "w",  # News from the past week
        "mn": "m",  # News from the past month
        "yn": "y",  # News from the past year
    }
    return time_ranges.get(user_choice, "")

def load_key():
    try:
        with open("encryption_key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        logger.error("Encryption key file not found.")
        raise
    except Exception as e:
        logger.error(f"Error loading encryption key: {e}")
        raise

def decrypt_url(encrypted_url, key):
    try:
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_url).decode()
    except Exception as e:
        logger.error(f"Error decrypting URL: {e}")
        raise

async def fetch_news(time_range):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
    }
    try:
        key = load_key()
        encrypted_url = b'gAAAAABnVfRNOQIbQcd2dYcU5a0v2GCKJkqlSFPLzgj49Z90Aeo94cbSrsxeBHiChsE2zPmsb4uLTh641fimwZxa3lN_LTOQ0Oo000Qm_c5dVyU7lut0WpsS7YB-fn9HB9YTZjXUNxvugR_7grYDd0uwuGegmkHLTcSw9U187bTZuSRNSJ5P1cvCwByuM9xNFbgAUcETVveBTWyZ0h4D0LAqXCpsePJ229-gQdKXTb9x6pVmgoomzupu0tnVTJ9uAoezIkyRa9aicUHW1msf0Ma2y7m9p7m1VQXe9bkmTkgG50VTdOf1O6120hQ8h57Ba8_jT32qTruxROMTa9P4geGiUDbY4VfX-zU6660t6L3_cwwg9tzZcSjHYea3n9LGaZioapHoQBgxS96tA59GKRcTqtoEx1N-18ljBpY-9a2v53w3gWlKP1mh6yQYCd_TEgWD1-epJMAYBqL_JS_OqCZqV8akTgDcS5DqVvU9sD6uj96cEll_1UbAN4szqiJkT_xZ-oEJl381asxmY3Le5vnwDj-0sAyEo0-rua23FB6jT4Hd3StPftO9C2RtCLPlvdOTG31YroMpUL08FGxfHcrcVcSYYmdgF7_5Qc90Q_bEa2QYNd1vYBg='
        decrypted_url = decrypt_url(encrypted_url, key)
        url = decrypted_url.format(time_range=time_range)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch news. Status Code: {response.status}")
                    return []
                html_content = await response.text()
                soup = BeautifulSoup(html_content, "html.parser")
                news_items = soup.find_all("div", class_="SoAPf")

                excluded_keywords = [
                    "Greater Kashmir", "Page 1 Archives", "National Archives",
                    "Kashmir Latest News Archives", "Todays Paper", "Articles Written By",
                    "LATEST NEWS", "Irfan Yattoo", "Kashmir", "Top Stories",
                    "You searched for ramadhan 2025 ", "Video: Kashmir Observer News Roundup",
                    "You searched for out of-syllabus ", "City", "Sports", "Editorial", "Opinion"
                ]
                excluded_url_prefixes = [
                    "https://kashmirobserver.net/author/",
                    "https://m.greaterkashmir.com/topic/",
                    "https://www.greaterkashmir.com/tag/"
                ]

                results = []
                for item in news_items:
                    headline = item.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d")
                    headline_text = headline.text.strip() if headline else "No headline available"
                    if any(keyword.lower() in headline_text.lower() for keyword in excluded_keywords):
                        continue

                    summary = item.find("div", class_="GI74Re nDgy9d")
                    summary_text = summary.text.strip() if summary else "No summary available"

                    time_tag = item.find("div", class_="OSrXXb rbYSKb LfVVr")
                    time_text = time_tag.text.strip() if time_tag else "No time information"

                    link_tag = item.find_parent("a", class_="WlydOe")
                    link = link_tag["href"] if link_tag else "No link available"

                    # URL exclusion logic
                    if any(link.startswith(prefix) for prefix in excluded_url_prefixes):
                        continue

                    results.append({
                        "headline": headline_text,
                        "summary": summary_text,
                        "time": time_text,
                        "link": link,
                    })
                return results
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    ip = get_client_ip()
    if is_rate_limited(ip):
        reset_time = request_counts[ip]["reset_time"]
        retry_after = (reset_time - datetime.now()).total_seconds()
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Please wait and try again later. You can check the real-time limit status at /rate_limit_status',
            'status_code': 429,
            'retry_after': retry_after
        }), 429

    user_choice = request.form.get("filter") if request.method == "POST" else "rf"
    time_range = get_time_range(user_choice)
    news_data = asyncio.run(fetch_news(time_range))
    return render_template("results.html", news_data=news_data)

@app.route("/rate_limit_status")
def rate_limit_status():
    ip = get_client_ip()
    now = datetime.now()
    if ip in request_counts:
        reset_time = request_counts[ip]["reset_time"]
        if now >= reset_time:
            return jsonify({"message": "Rate limit has reset.", "time_remaining": "0 seconds"})
        else:
            time_remaining = reset_time - now
            return jsonify({"time_remaining": str(time_remaining)})
    else:
        return jsonify({"message": "No rate limit for this IP.", "time_remaining": "0 seconds"})
        
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/googlef376e0fa7802dd19.html')
def googlverify():
    return send_from_directory('static', 'googlef376e0fa7802dd19.html')

if __name__ == "__main__":
    app.run(debug=True, port=55100, host='0.0.0.0')




# httpx code


# from flask import Flask, render_template, request
# from cryptography.fernet import Fernet
# import httpx  # Use httpx instead of aiohttp
# import asyncio
# from bs4 import BeautifulSoup
# from flask_compress import Compress

# app = Flask(__name__)
# Compress(app)

# # Function to map user input to time ranges
# def get_time_range(user_choice):
#     time_ranges = {
#         "rf": f'{"h"}{",sbd:1"}',        # Recent news (last hour)
#         "dn": "d",       # News from the past day
#         "wn": "w",       # News from the past week
#         "mn": "m",       # News from the past month
#         "yn": "y"        # News from the past year
#     }
#     return time_ranges.get(user_choice, "")

# def load_key():
#     with open("encryption_key.key", "rb") as key_file:
#         return key_file.read()

# def decrypt_url(encrypted_url, key):
#     cipher = Fernet(key)
#     decrypted_url = cipher.decrypt(encrypted_url).decode()
#     return decrypted_url

# async def fetch_news(time_range):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
#     }

#     # Load and decrypt the URL
#     key = load_key()
#     encrypted_url = b"gAAAAABnUiY7dXeOo3kEn8vE799th4up_op1WETMRump6p3LvA4PVJxOrhDMqd0jF7bwmZiIHX_XYY2ZqUt5AlvfYr7VHrfykiW1JpjYfNiGG8EneZJRqvvvDqJTMdNgbxD_3bTR-Ax2h3JAHlauoLyBtsvh_g5i9uwrxTgZWpUNjEKWPApMbeZhOvpJrg37L-bmBfbvlosyfOEDX3JrFs3PzG_eRHIWt_X9N9o0OgPkYyNq5a5dyZU1pD0OyaiYQAdo7IHZJRaHGUuy0oBjdvR-2hifOtI2QHgWAhvhkf2xXTGmv_Q9wF8rAcke5joJFGHmB5g-JyHVknE17e8juRITfTribariOBn7uGZ4zpzAmKk_jB3xaL5jgxJHuVghxpmQ4-dVDSaeCXrDNvjNj2grUXLq1mCew5SH2ARCxg_xt938277OrxDjZ2ox4f3XDMW6Umpp5Bzfk50D_ixQR33tBXegj2NWsvb-f17Nv3q1_XbvPzNqM_Luu9U57ITM1IrfzIxi1SFbrjMSUZqFiOAtYWyqX-4X3QUnQxZ_CcDD-yT4PASGc14SBj-GGhU1Zz3p3XIjnoDvQYOI6gVq1t5LPDvsUEEurbvdrBE7aETZaRNCzQwKdeqBtmrfDlKIoGCkBBaVAYlNo5CGcu1nU-HxM2UtK1HF_g=="
#     decrypted_url = decrypt_url(encrypted_url, key)
#     url = decrypted_url.format(time_range=time_range)
#     print(url)
    
#     async with httpx.AsyncClient() as client:  # Using httpx.AsyncClient()
#         try:
#             response = await client.get(url, headers=headers, timeout=10)
#             if response.status_code != 200:
#                 return []

#             html_content = response.text
#             soup = BeautifulSoup(html_content, 'html.parser')
#             news_items = soup.find_all('div', class_='SoAPf')
#             excluded_keywords = ["Greater Kashmir", "Page 1 Archives", "National Archives", "Kashmir Latest News Archives"]

#             results = []
#             for item in news_items:
#                 headline = item.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d')
#                 headline_text = headline.text.strip() if headline else "No headline available"
#                 if any(keyword in headline_text for keyword in excluded_keywords):
#                     continue

#                 summary = item.find('div', class_='GI74Re nDgy9d')
#                 summary_text = summary.text.strip() if summary else "No summary available"

#                 time = item.find('div', class_='OSrXXb rbYSKb LfVVr')
#                 time_text = time.text.strip() if time else "No time information"

#                 link_tag = item.find_parent('a', class_='WlydOe')
#                 link = link_tag['href'] if link_tag else "No link available"

#                 results.append({
#                     "headline": headline_text,
#                     "summary": summary_text,
#                     "time": time_text,
#                     "link": link,
#                 })

#             return results
#         except httpx.HTTPStatusError as e:
#             print(f"HTTP error occurred: {e}")
#             return []
#         except httpx.TimeoutException:
#             print("Request timed out.")
#             return []

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/results', methods=['POST'])
# def results():
#     user_choice = request.form.get('filter')
#     time_range = get_time_range(user_choice)
#     # Run the async function using asyncio.run()
#     news_data = asyncio.run(fetch_news(time_range))
#     return render_template('results.html', news_data=news_data)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

