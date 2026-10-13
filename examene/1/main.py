from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url:", build_url("example.com", "/login"))
print("Partea 1, is_https:", is_https("https://example.com"))
print("Partea 1, is_https:", is_https("http://example.com"))

print("Partea 2, show_response:")
show_response("https://example.com")
show_response("https://httpbin.org/status/404")

print("Partea 3, check_site:", check_site("https://example.com"))
print("Partea 3, check_site:", check_site("http://this-site-does-not-exist.invalid"))

print("Partea 4, scan_sites:")
scan_sites()

print("Partea 5, check_headers:", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers:", check_headers("https://example.com"))

print("Partea 6, retry_check:", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check:", retry_check("https://httpbin.org/status/404"))
