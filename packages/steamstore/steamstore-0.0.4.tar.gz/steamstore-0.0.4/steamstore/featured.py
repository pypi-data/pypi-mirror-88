
class FeaturedItem():
    def __init__(self, *, data):
        self.id = data["id"]
        self.type = data["type"]
        self.name = data["name"]
        self.discounted = data["discounted"]
        self.discount_percent = data["discount_percent"]
        self.original_price = data["original_price"]
        self.final_price = data["final_price"]
        self.currency = data["currency"]
        self.large_capsule_image = data["large_capsule_image"]
        self.small_capsule_image = data["small_capsule_image"]
        self.windows_available = data["windows_available"]
        self.mac_available = data["mac_available"]
        self.linux_available = data["linux_available"]
        self.streamingvideo_available = data["streamingvideo_available"]
        self.discount_expiration = data["discount_expiration"] if "discount_expiration" in data else None
        self.header_image = data["header_image"]
        self.controller_support = data["controller_support"] if "controller_support" in data else None

class FeaturedList():
    def __init__(self, *, data):
        self.large_capsules = [FeaturedItem(data=item) for item in data["large_capsules"]]
        self.featured_win = [FeaturedItem(data=item) for item in data["featured_win"]]
        self.featured_mac = [FeaturedItem(data=item) for item in data["featured_mac"]]
        self.featured_linux = [FeaturedItem(data=item) for item in data["featured_linux"]]
        self.layout = data["layout"]
        self.status = data["status"]
