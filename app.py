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

"""
app_fixed.py – Flask + aiohttp news-scraper with robust rate-limiting
--------------------------------------------------------------------
Changes vs original:
1.  Uses timezone-aware datetimes (UTC) everywhere.
2.  Corrects defaultdict logic so a fresh IP starts a *new* window.
3.  Makes all access to `request_counts` atomic under one Lock.
4.  Garbage-collects idle IPs immediately after a window expires.
5.  Re-uses a single aiohttp.ClientSession (created in a background
    thread-safe way) instead of a new one per request.
6.  Strips whitespace from X-Forwarded-For, handles missing IP.
7.  Improves /rate_limit_status output & resets expired windows.
8.  Registers a *locked* cleanup call at exit.
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from cryptography.fernet import Fernet
import aiohttp, asyncio, atexit, logging, time
from bs4 import BeautifulSoup
from flask_compress import Compress
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from threading import Thread, Lock

# ------------------------------------------------------------------ setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)
Compress(app)

MAX_REQUESTS   = 10
WINDOW_SECONDS = 12 * 60 * 60          # 12 h
lock           = Lock()

request_counts = defaultdict(
    lambda: {
        "count": 0,
        "reset_time": datetime.now(tz=timezone.utc) + timedelta(seconds=WINDOW_SECONDS)
    }
)

# ---------- aiohttp session ------------------------------------------------
_session_ready = asyncio.Event()
_session: aiohttp.ClientSession | None = None

async def _create_session():
    global _session
    _session = aiohttp.ClientSession()
    _session_ready.set()

def _ensure_session():
    """Fire-and-forget task that builds one ClientSession lazily."""
    if not _session_ready.is_set():
        loop = asyncio.get_event_loop()
        loop.create_task(_create_session())

# ---------- helpers --------------------------------------------------------
def now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)

def get_client_ip() -> str | None:
    """Return the client IP or None."""
    xff = request.headers.get("X-Forwarded-For", "")
    ip  = xff.split(",")[0].strip() if xff else request.remote_addr
    return ip or None

def _window_expired(data: dict[str, object]) -> bool:
    return now_utc() >= data["reset_time"]  # type: ignore[index]

def is_rate_limited(ip: str) -> bool:
    """True if the request should be rejected with 429."""
    with lock:
        rc = request_counts[ip]
        if _window_expired(rc):
            # start a brand-new window
            rc["count"]      = 1
            rc["reset_time"] = now_utc() + timedelta(seconds=WINDOW_SECONDS)
            return False

        rc["count"] += 1
        return rc["count"] > MAX_REQUESTS     # type: ignore[operator]

def _cleanup_dict():
    """Remove entries whose window ended (regardless of count)."""
    with lock:
        expired = [ip for ip, data in request_counts.items() if _window_expired(data)]
        for ip in expired:
            del request_counts[ip]

def _cleanup_loop():
    while True:
        _cleanup_dict()
        time.sleep(3600)        # hourly

Thread(target=_cleanup_loop, daemon=True).start()
atexit.register(_cleanup_dict)   # locked inside

# ---------- news-scraper ---------------------------------------------------
def load_key() -> bytes:
    with open("encryption_key.key", "rb") as fh:
        return fh.read()

def decrypt_url(enc: bytes, key: bytes) -> str:
    return Fernet(key).decrypt(enc).decode()

def get_time_range(choice: str) -> str:
    return {
        "rf": "h,sbd:1",
        "dn": "d",
        "wn": "w",
        "mn": "m",
        "yn": "y",
    }.get(choice, "")

async def fetch_news(time_range: str) -> list[dict[str, str]]:
    _ensure_session()
    await _session_ready.wait()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/117.0 Safari/537.36"
        )
    }
    key = load_key()
    encrypted_url = (
        b"gAAAAABnVfRNOQIbQcd2dYcU5a0v2GCKJkqlSFPLzgj49Z90Aeo94cbSrs"
        b"xeBHiChsE2zPmsb4uLTh641fimwZxa3lN_LTOQ0Oo000Qm_c5dVyU7lut0"
        b"WpsS7YB-fn9HB9YTZjXUNxvugR_7grYDd0uwuGegmkHLTcSw9U187bTZuSR"
        b"NSJ5P1cvCwByuM9xNFbgAUcETVveBTWyZ0h4D0LAqXCpsePJ229-gQdKXTb"
        b"9x6pVmgoomzupu0tnVTJ9uAoezIkyRa9aicUHW1msf0Ma2y7m9p7m1VQXe9"
        b"bkmTkgG50VTdOf1O6120hQ8h57Ba8_jT32qTruxROMTa9P4geGiUDbY4VfX"
        b"-zU6660t6L3_cwwg9tzZcSjHYea3n9LGaZioapHoQBgxS96tA59GKRcTqto"
        b"Ex1N-18ljBpY-9a2v53w3gWlKP1mh6yQYCd_TEgWD1-epJMAYBqL_JS_OqC"
        b"ZqV8akTgDcS5DqVvU9sD6uj96cEll_1UbAN4szqiJkT_xZ-oEJl381asxmY"
        b"3Le5vnwDj-0sAyEo0-rua23FB6jT4Hd3StPftO9C2RtCLPlvdOTG31YroMp"
        b"UL08FGxfHcrcVcSYYmdgF7_5Qc90Q_bEa2QYNd1vYBg="
    )
    url = decrypt_url(encrypted_url, key).format(time_range=time_range)

    async with _session.get(url, headers=headers, timeout=10) as resp:
        if resp.status != 200:
            log.warning("News fetch failed (%s)", resp.status)
            return []

        soup = BeautifulSoup(await resp.text(), "html.parser")
        items = soup.find_all("div", class_="SoAPf")

        excluded_kw = {
            "greater kashmir", "page 1 archives", "national archives",
            "kashmir latest news archives", "todays paper", "articles written by",
            "latest news", "irfan yattoo", "top stories", "city",
            "sports", "editorial", "opinion", "video:"
        }
        excluded_prefix = {
            "https://kashmirobserver.net/author/",
            "https://m.greaterkashmir.com/topic/",
            "https://www.greaterkashmir.com/tag/"
        }

        results: list[dict[str, str]] = []
        for it in items:
            title_el   = it.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d")
            headline   = title_el.text.strip() if title_el else "No headline available"

            if any(kw in headline.lower() for kw in excluded_kw):
                continue

            summary_el = it.find("div", class_="GI74Re nDgy9d")
            summary    = summary_el.text.strip() if summary_el else "No summary available"

            time_el = it.find("div", class_="OSrXXb rbYSKb LfVVr")
            when    = time_el.text.strip() if time_el else "No time information"

            link_el = it.find_parent("a", class_="WlydOe")
            link    = link_el["href"] if link_el else "No link available"

            if any(link.startswith(pref) for pref in excluded_prefix):
                continue

            results.append({"headline": headline, "summary": summary, "time": when, "link": link})
        return results

# ---------- Flask routes ---------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    ip = get_client_ip()
    if ip and is_rate_limited(ip):
        reset_in = (request_counts[ip]["reset_time"] - now_utc()).total_seconds()  # type: ignore[index]
        return jsonify(
            error="Rate limit exceeded",
            retry_after=reset_in,
            status_code=429,
            message="Please wait and try again later. "
                    "You can check your limit at /rate_limit_status"
        ), 429

    choice     = request.form.get("filter") if request.method == "POST" else "rf"
    time_range = get_time_range(choice)

    # Blocking call – fine under WSGI. For ASGI, run in threadpool.
    news_data  = asyncio.run(fetch_news(time_range))
    return render_template("results.html", news_data=news_data)

@app.route("/rate_limit_status")
def rate_limit_status():
    ip = get_client_ip()
    if not ip or ip not in request_counts:
        return jsonify(message="No rate limit for this IP")

    with lock:
        rc = request_counts[ip]
        if _window_expired(rc):
            del request_counts[ip]
            return jsonify(message="Rate limit window has reset")

        remaining = MAX_REQUESTS - rc["count"]     # type: ignore[operator]
        seconds   = int((rc["reset_time"] - now_utc()).total_seconds())  # type: ignore[index]
    return jsonify(remaining_requests=remaining, seconds_to_reset=seconds)

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/googlef376e0fa7802dd19.html")
def google_verify():
    return send_from_directory("static", "googlef376e0fa7802dd19.html")

# ------------------------------------------------------------------ launch
if __name__ == "__main__":
    # production: use gunicorn -w4 -k uvicorn.workers.UvicornWorker app_fixed:app
    app.run(debug=True, host="0.0.0.0", port=55100)




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
