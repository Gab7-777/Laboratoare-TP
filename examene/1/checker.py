import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    if not path.startswith("/"):
        path = "/" + path
    return "https://" + host + path


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.exceptions.RequestException as error:
        print("Error:", str(error))


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get("Content-Type", "unknown")
        content_type = content_type.split(";")[0]
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.exceptions.RequestException as error:
        return {"status": None, "error": str(error)}


def scan_sites():
    results = []
    for site in SITES:
        result = check_site(site)
        result["url"] = site
        results.append(result)

    working_sites = []
    failed_sites = 0

    for result in results:
        if result["status"] == 200:
            working_sites.append(result)
        else:
            failed_sites += 1

    working_sites.sort(key=lambda result: result["length"], reverse=True)

    for result in working_sites:
        print(result["url"], "->", result["status"], ",", result["length"], "octeți")

    print("Reușite:", len(working_sites), "| Eșuate:", failed_sites)


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header in response.headers:
                present.append(header)
            else:
                missing.append(header)

        score = int(len(present) / len(SECURITY_HEADERS) * 100)
        return {"present": present, "missing": missing, "score": score}
    except requests.exceptions.RequestException as error:
        return {"status": None, "error": str(error)}


def retry_check(url, attempts=3):
    number_of_attempts = 0
    last_status = None
    last_error = None

    while number_of_attempts < attempts:
        number_of_attempts += 1
        print(f"Attempt {number_of_attempts} for {url}")
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code

            if response.status_code < 500:
                return {
                    "status": response.status_code,
                    "attempts": number_of_attempts,
                }
        except requests.exceptions.RequestException as error:
            last_error = str(error)

    result = {"status": last_status, "attempts": number_of_attempts}
    if last_status is None:
        result["error"] = last_error
    return result
