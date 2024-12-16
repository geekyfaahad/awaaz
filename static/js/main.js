const domains = [
    "https://kashmirobserver.net",
    "https://thekashmiriyat.co.uk",
    "https://kashmirnews.in",
    "https://kashmirdespatch.com",
    "https://kashmirlife.net",
    "https://risingkashmir.com",
    "https://greaterkashmir.com",
    "https://asiannewshub.com",
    "https://thekashmirmonitor.net",
    "https://kashmirreader.com",
    "https://kashmirtimes.com",
    "https://newsvibesofindia.com",
    "https://kashmirvision.in"
];
function createLink(rel, href, crossorigin = false) {
    const link = document.createElement("link");
    link.rel = rel;
    link.href = href;
    if (crossorigin) {
        link.crossOrigin = "anonymous";
    }
    document.head.appendChild(link);
}
domains.forEach(domain => {
    createLink("preconnect", domain, true);
    createLink("dns-prefetch", domain);
});



function checkInternetConnection() {
  const checkConnection = async () => {
    try {
      const response = await fetch("https://www.google.com", {
        method: "HEAD",
        cache: "no-cache",
      });
      if (response.ok) {
        console.log("Internet connection is active.");
      } else {
        console.warn("Internet connection seems to be offline.");
      }
    } catch (error) {
      console.error("No internet connection or request failed.", error);
    }
  };

  // Check immediately and then every 14 minutes
  checkConnection(); // Initial check
  setInterval(checkConnection, 14 * 60 * 1000); // 14 minutes in milliseconds
}

// Call the function
checkInternetConnection();
