from django.contrib.gis.geoip2 import GeoIP2


def get_location(request):
    g = GeoIP2()
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    if ip == "127.0.0.1":
        city = {"city": "localhost"}
    elif ip:
        city = g.city(ip)
    else:
        city = {"city": "Unknown"}
    return city
