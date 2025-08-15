
# aiohttp code


from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
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
from urllib.parse import urlparse
import json
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
Compress(app)

# Firebase configuration
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAIY-rRT3cTHCPClUMYBsqKi0odJ1by1bQ",
    "authDomain": "awaaz-e8330.firebaseapp.com",
    "projectId": "awaaz-e8330",
    "storageBucket": "awaaz-e8330.firebasestorage.app",
    "messagingSenderId": "1070192874849",
    "appId": "1:1070192874849:web:257894ce51625f35c7a120",
    "measurementId": "G-R6EFGZBLK9"
}

# Initialize Firebase Admin SDK
try:
    # Use service account key if available, otherwise use default credentials
    if os.path.exists('firebase-service-account.json'):
        cred = credentials.Certificate('firebase-service-account.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info("Firebase Admin SDK initialized successfully with service account")
    else:
        # For local development without Firebase credentials, use default sources
        logger.info("No Firebase credentials found. Using default news sources.")
        db = None
except Exception as e:
    logger.error(f"Failed to initialize Firebase: {e}")
    db = None

rate_limit = 100
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

# Default news sources
DEFAULT_NEWS_SOURCES = [
    {"domain": "kashmirobserver.net", "name": "Kashmir Observer", "enabled": True},
    {"domain": "thekashmiriyat.co.uk", "name": "The Kashmiriyat", "enabled": True},
    {"domain": "kashmirnews.in", "name": "Kashmir News", "enabled": True},
    {"domain": "kashmirdespatch.com", "name": "Kashmir Dispatch", "enabled": True},
    {"domain": "kashmirlife.net", "name": "Kashmir Life", "enabled": True},
    {"domain": "greaterkashmir.com", "name": "Greater Kashmir", "enabled": True},
    {"domain": "asiannewshub.com", "name": "Asian News Hub", "enabled": True},
    {"domain": "thekashmirmonitor.net", "name": "The Kashmir Monitor", "enabled": True},
    {"domain": "kashmirtimes.com", "name": "Kashmir Times", "enabled": True},
    {"domain": "newsvibesofindia.com", "name": "News Vibes of India", "enabled": True},
    {"domain": "kashmirvision.in", "name": "Kashmir Vision", "enabled": True}
]

############################
# Local storage (fallback) #
############################

LOCAL_DATA_DIR: Path = Path("data")
LOCAL_SOURCES_FILE: Path = LOCAL_DATA_DIR / "news_sources.json"
_sources_file_lock: Lock = Lock()

def _ensure_local_sources_file_exists() -> None:
    if not LOCAL_DATA_DIR.exists():
        LOCAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOCAL_SOURCES_FILE.exists():
        # Seed with defaults and deterministic ids (use domain as id)
        seeded = []
        for src in DEFAULT_NEWS_SOURCES:
            seeded.append({**src, "id": src["domain"]})
        with _sources_file_lock:
            LOCAL_SOURCES_FILE.write_text(json.dumps(seeded, indent=2), encoding="utf-8")

def load_local_sources() -> list:
    _ensure_local_sources_file_exists()
    with _sources_file_lock:
        try:
            raw = LOCAL_SOURCES_FILE.read_text(encoding="utf-8")
            sources = json.loads(raw)
            # Ensure each has id
            for s in sources:
                if "id" not in s:
                    s["id"] = s.get("domain")
            return sources
        except Exception as e:
            logger.error(f"Failed to read local sources: {e}")
            # Fall back to defaults if read fails
            seeded = [{**s, "id": s["domain"]} for s in DEFAULT_NEWS_SOURCES]
            return seeded

def save_local_sources(sources: list) -> None:
    with _sources_file_lock:
        try:
            LOCAL_SOURCES_FILE.write_text(json.dumps(sources, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to write local sources: {e}")

def toggle_source_local(source_id: str, enabled: bool) -> bool:
    sources = load_local_sources()
    updated = False
    for s in sources:
        if s.get("id") == source_id or s.get("domain") == source_id:
            s["enabled"] = enabled
            updated = True
            break
    if updated:
        save_local_sources(sources)
    return updated

def add_source_local(domain: str, name: str) -> bool:
    domain = (domain or "").strip().lower()
    name = (name or "").strip()
    if not domain or not name:
        return False
    sources = load_local_sources()
    # Prevent duplicates by domain
    for s in sources:
        if s.get("domain").lower() == domain:
            return False
    sources.append({"id": domain, "domain": domain, "name": name, "enabled": True})
    save_local_sources(sources)
    return True

def delete_source_local(source_id: str) -> bool:
    sources = load_local_sources()
    new_sources = [s for s in sources if s.get("id") != source_id and s.get("domain") != source_id]
    if len(new_sources) == len(sources):
        return False
    save_local_sources(new_sources)
    return True

def initialize_news_sources():
    """Initialize news sources in Firebase if they don't exist"""
    if db is None:
        # Initialize local file
        _ensure_local_sources_file_exists()
        logger.info("Initialized local news_sources.json store")
        return
    try:
        sources_ref = db.collection('news_sources')
        existing_sources = [doc.to_dict() for doc in sources_ref.stream()]
        if not existing_sources:
            for source in DEFAULT_NEWS_SOURCES:
                sources_ref.add(source)
            logger.info("News sources initialized in Firebase")
        else:
            logger.info("News sources already exist in Firebase")
    except Exception as e:
        logger.error(f"Error initializing news sources: {e}")

def get_news_sources():
    """Get news sources from Firebase"""
    if db is None:
        return load_local_sources()
    try:
        sources_ref = db.collection('news_sources')
        sources = []
        for doc in sources_ref.stream():
            source_data = doc.to_dict()
            source_data['id'] = doc.id
            sources.append(source_data)
        return sources
    except Exception as e:
        logger.error(f"Error getting news sources: {e}")
        # Fallback to local
        return load_local_sources()

def is_admin_authenticated():
    """Check if user is authenticated as admin"""
    return session.get('admin_authenticated', False)

def require_admin_auth(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        if not is_admin_authenticated():
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

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
        # encrypted_url = b'gAAAAABonzkH9afLF1lqpAoil2jfkRTNIgRaJUVwobB3yRTW8jf8pZ1q7uHb5WhmcDLe9wDyXXwbN8fXzsyOXLOoGeqKd1nbVez-EaCmVLYvQ3oDMLzUGEV7U1qIGIre80E-SOSH9Nbh18bt4KSmUBRLBED-0gy-73YR8S56eELQVQVnb75rtru2zRY5g2qbQpARP8gJZtORMHU5cjqrR8Aa8xWzEzYR97mbCrxOnPv_O-kgstkrfVGNaTiORfcQVk9IQutcTLNYI__SKSttz9FdKUoY5u5Ge_e19qK7Td8tP8tmqTAmzZdLK6_VntYZzh4TbnDMAlMADhimLi0-I-1GTy8fOx7esf0pw-5oJBwtpXxunwEGhQlINAUoq6urE51doCnC7O9pSEiP1hZr3ogiSfX8QUp0PCtkUlPdPb_5P-EF-Ppu3OQ_sEX3RRcPZuDQb1I_SXgtUjHniS7Jeko1Vp1cy7NCZ4odsIJOYElm2P2kEsSl0QTxVS5l_O2X80183l0EyPXUQi7bWwd9K5YYwqEYYrAM_yJUEzsKC48tkRDqjTEHhyu7mbBvUxroZhe_yN3z5LUa'
        # decrypted_url = decrypt_url(encrypted_url, key)
        # Get enabled news sources
        news_sources = get_news_sources()
        enabled_sources = [source['domain'] for source in news_sources if source.get('enabled', True)]
        
        if not enabled_sources:
            logger.warning("No news sources are enabled")
            return []
        
        # Build search query with enabled sources
        sources_query = "+OR+".join([f"site:{domain}" for domain in enabled_sources])
        url = f"https://www.google.com/search?q={sources_query}+News&sca_esv=75315e11642a04a4&tbs=qdr:{time_range}&tbm=nws"

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
                    "https://www.greaterkashmir.com/tag/",
                    "https://kashmirlife.net/tag/",
                    "https://www.kashmirlife.net/tag/"
                ]
                
                # Page numbers to exclude (add specific page numbers you want to avoid)
                excluded_page_numbers = [
                    "page-1", "page-2", "page-3", "page-4", "page-5",  # Common page numbers
                    "p=1", "p=2", "p=3", "p=4", "p=5",  # Alternative page parameter format
                    "/1/", "/2/", "/3/", "/4/", "/5/",  # URL path page numbers
                    "page1", "page2", "page3", "page4", "page5"  # Without hyphens
                ]

                results = []
                
                # Process all news items first to collect basic info
                news_items_data = []
                for item in news_items:
                    headline = item.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d")
                    headline_text = headline.text.strip() if headline else "No headline available"
                    
                    # Check if headline starts with page-related text
                    headline_lower = headline_text.lower()
                    if headline_lower.startswith(('page', 'page-', 'page ')):
                        continue
                    
                    # Check if headline starts with "you searched for" type text
                    if headline_lower.startswith(('you searched for', 'you searched', 'searched for')):
                        continue
                    
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

                    # Page number exclusion logic
                    if any(page_num in link.lower() for page_num in excluded_page_numbers):
                        continue
                    
                    # Also check headline for page numbers
                    if any(page_num in headline_text.lower() for page_num in excluded_page_numbers):
                        continue

                    news_items_data.append({
                        "headline": headline_text,
                        "summary": summary_text,
                        "time": time_text,
                        "link": link,
                    })
                
                # Now extract images concurrently for better performance
                async def extract_image_for_article(article_data):
                    image_url = "No image available"
                    try:
                        # Fetch the actual article page to get the image
                        async with session.get(article_data["link"], headers=headers, timeout=10) as article_response:
                            if article_response.status == 200:
                                article_html = await article_response.text()
                                article_soup = BeautifulSoup(article_html, "html.parser")
                                
                                # FIRST PRIORITY: Try Open Graph and social media meta tags (what WhatsApp uses)
                                meta_selectors = [
                                    'meta[property="og:image"]',
                                    'meta[property="og:image:secure_url"]',
                                    'meta[name="twitter:image"]',
                                    'meta[name="twitter:image:src"]',
                                    'meta[property="og:image:url"]',
                                    'meta[name="image"]'
                                ]
                                
                                for selector in meta_selectors:
                                    meta_tag = article_soup.select_one(selector)
                                    if meta_tag:
                                        image_url = meta_tag.get("content", "")
                                        if image_url and image_url != "No image available":
                                            # Handle relative URLs for meta tags
                                            if image_url.startswith("//"):
                                                image_url = "https:" + image_url
                                            elif image_url.startswith("/"):
                                                parsed_link = urlparse(article_data["link"])
                                                if parsed_link.netloc:
                                                    image_url = f"https://{parsed_link.netloc}{image_url}"
                                            logger.info(f"Found Open Graph image: {image_url[:100]}...")
                                            break
                                
                                # SECOND PRIORITY: Try to find images with common selectors
                                if image_url == "No image available":
                                    img_selectors = [
                                        "img[src*='.jpg']", "img[src*='.jpeg']", "img[src*='.png']", "img[src*='.webp']",
                                        ".article-image img", ".post-image img", ".featured-image img",
                                        ".entry-image img", ".content-image img", ".main-image img",
                                        ".hero-image img", ".banner-image img", ".thumbnail img",
                                        "article img", ".article img", ".post img", ".content img",
                                        ".story-image img", ".news-image img", ".media img"
                                    ]
                                    
                                    for selector in img_selectors:
                                        img_tag = article_soup.select_one(selector)
                                        if img_tag:
                                            image_url = img_tag.get("src", "")
                                            if image_url and image_url != "No image available":
                                                # Handle relative URLs
                                                if image_url.startswith("//"):
                                                    image_url = "https:" + image_url
                                                elif image_url.startswith("/"):
                                                    parsed_link = urlparse(article_data["link"])
                                                    if parsed_link.netloc:
                                                        image_url = f"https://{parsed_link.netloc}{image_url}"
                                                logger.info(f"Found selector image: {image_url[:100]}...")
                                                break
                                
                                # THIRD PRIORITY: Try finding any image with reasonable size
                                if image_url == "No image available":
                                    all_images = article_soup.find_all("img")
                                    for img in all_images:
                                        src = img.get("src", "")
                                        if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                            # Check if image has reasonable dimensions or is likely to be a content image
                                            width = img.get("width", "")
                                            height = img.get("height", "")
                                            alt = img.get("alt", "").lower()
                                            
                                            # Skip small images, icons, or likely non-content images
                                            if (width and int(width) < 100) or (height and int(height) < 100):
                                                continue
                                            if any(skip_word in alt for skip_word in ['icon', 'logo', 'avatar', 'profile']):
                                                continue
                                            
                                            # Handle relative URLs
                                            if src.startswith("//"):
                                                image_url = "https:" + src
                                            elif src.startswith("/"):
                                                parsed_link = urlparse(article_data["link"])
                                                if parsed_link.netloc:
                                                    image_url = f"https://{parsed_link.netloc}{src}"
                                            else:
                                                image_url = src
                                            logger.info(f"Found fallback image: {image_url[:100]}...")
                                            break
                                
                    except Exception as e:
                        logger.warning(f"Error extracting image from {article_data['link']}: {e}")
                        image_url = "No image available"
                    
                    # Log image extraction results for debugging
                    if image_url == "No image available":
                        logger.info(f"No image found for: {article_data['headline'][:50]}...")
                        # Provide a fallback image based on the domain
                        try:
                            parsed_link = urlparse(article_data["link"])
                            domain = parsed_link.netloc.lower()
                            if "greaterkashmir" in domain:
                                image_url = "https://via.placeholder.com/400x200/3f51b5/ffffff?text=Greater+Kashmir+News"
                            elif "kashmirobserver" in domain:
                                image_url = "https://via.placeholder.com/400x200/ff5722/ffffff?text=Kashmir+Observer"
                            elif "kashmirnews" in domain:
                                image_url = "https://via.placeholder.com/400x200/4caf50/ffffff?text=Kashmir+News"
                            elif "kashmirlife" in domain:
                                image_url = "https://via.placeholder.com/400x200/9c27b0/ffffff?text=Kashmir+Life"
                            else:
                                image_url = "https://via.placeholder.com/400x200/607d8b/ffffff?text=Kashmir+News"
                        except:
                            image_url = "https://via.placeholder.com/400x200/607d8b/ffffff?text=News+Article"
                        logger.info(f"Using fallback image: {image_url}")
                    else:
                        logger.info(f"✅ SUCCESS: Image found for '{article_data['headline'][:50]}...' -> {image_url}")
                    
                    return {**article_data, "image": image_url}
                
                # Extract images concurrently for better performance
                if news_items_data:
                    tasks = [extract_image_for_article(item) for item in news_items_data]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Filter out any exceptions and ensure we have valid results
                    valid_results = []
                    for result in results:
                        if isinstance(result, Exception):
                            logger.error(f"Error processing article: {result}")
                            continue
                        valid_results.append(result)
                    
                    return valid_results
                
                return []
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

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple admin authentication (you should use proper authentication)
        if username == 'admin' and password == 'admin123':  # Change these credentials
            session['admin_authenticated'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@require_admin_auth
def admin_dashboard():
    news_sources = get_news_sources()
    last_updated_str = datetime.now().strftime('%B %d, %Y, %I:%M:%S %p')
    return render_template('admin_dashboard.html', news_sources=news_sources, last_updated=last_updated_str)

@app.route('/admin/sources', methods=['GET', 'POST'])
@require_admin_auth
def admin_sources():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'toggle':
            source_id = request.form.get('source_id')
            enabled = request.form.get('enabled') == 'true'
            
            # If Firestore available, try it; otherwise use local storage
            if db is not None:
                try:
                    db.collection('news_sources').document(source_id).update({'enabled': enabled})
                    return jsonify({'success': True, 'message': 'Source updated successfully'})
                except Exception as e:
                    logger.warning(f"Firestore update failed for toggle, falling back to local: {e}")
            # Local fallback
            if toggle_source_local(source_id, enabled):
                return jsonify({'success': True, 'message': 'Source updated successfully (local)'})
            return jsonify({'success': False, 'message': 'Error updating source'})
        
        elif action == 'add':
            domain = request.form.get('domain')
            name = request.form.get('name')
            
            if not domain or not name:
                return jsonify({'success': False, 'message': 'Domain and name are required'})
            
            if db is not None:
                try:
                    db.collection('news_sources').add({'domain': domain, 'name': name, 'enabled': True})
                    return jsonify({'success': True, 'message': 'Source added successfully'})
                except Exception as e:
                    logger.warning(f"Firestore add failed, falling back to local: {e}")
            if add_source_local(domain, name):
                return jsonify({'success': True, 'message': 'Source added successfully (local)'})
            return jsonify({'success': False, 'message': 'Error adding source (maybe duplicate domain?)'})
        
        elif action == 'delete':
            source_id = request.form.get('source_id')
            
            if db is not None:
                try:
                    db.collection('news_sources').document(source_id).delete()
                    return jsonify({'success': True, 'message': 'Source deleted successfully'})
                except Exception as e:
                    logger.warning(f"Firestore delete failed, falling back to local: {e}")
            if delete_source_local(source_id):
                return jsonify({'success': True, 'message': 'Source deleted successfully (local)'})
            return jsonify({'success': False, 'message': 'Error deleting source'})
    
    news_sources = get_news_sources()
    return render_template('admin_sources.html', news_sources=news_sources)

@app.route('/admin/api/sources', methods=['GET'])
@require_admin_auth
def api_sources():
    news_sources = get_news_sources()
    return jsonify(news_sources)

if __name__ == "__main__":
    # Initialize news sources on startup
    initialize_news_sources()
    app.run(debug=True, port=55100, host='0.0.0.0')
