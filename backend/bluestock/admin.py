from django.contrib.admin import AdminSite

class BluestockAdminSite(AdminSite):
    site_header = "Bluestock Administration"
    site_title = "Bluestock Admin"
    index_title = "Welcome to Bluestock Administration"

admin_site = BluestockAdminSite(name='admin') 