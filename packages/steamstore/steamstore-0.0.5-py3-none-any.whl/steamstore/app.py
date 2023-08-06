class EmptyRequirements:
    pass


class BaseRequirements(object):
    def __new__(self, *, data):
        if "minimum" not in data:
            return EmptyRequirements()
        
        self.__init__(self, data=data)
        return self

    def __init__(self, *, data):
        self.minimum = data["minimum"]
        self.recommended = data["recommended"] if "recommended" in data else None

class PcRequirements(BaseRequirements):
    pass

        
class MacRequirements(BaseRequirements):
    pass

class LinuxRequirements(BaseRequirements):
    pass

class Demo:
    def __init__(self, *, data):
        self.appid = data["appid"]
        self.description = data["description"]

class PriceOverview:
    def __init__(self, *, data):
        self.currency = data["currency"]
        self.initial = data["initial"]
        self.final = data["final"]
        self.discount_percent = data["discount_percent"]
        self.initial_formatted = data["initial_formatted"]
        self.final_formatted = data["final_formatted"]

class Sub:
    def __init__(self, *, data):
        self.packageid = data["packageid"]
        self.percent_savings_text = data["percent_savings_text"]
        self.percent_savings = data["percent_savings"]
        self.option_text = data["option_text"]
        self.option_description = data["option_description"]
        self.can_get_free_license = data["can_get_free_license"]
        self.is_free_license = data["is_free_license"]
        self.price_in_cents_with_discount = data["price_in_cents_with_discount"]

class PackageGroups:
    def __init__(self, *, data):
        self.name = data["name"]
        self.title = data["title"]
        self.description = data["description"]
        self.selection_text = data["selection_text"]
        self.save_text = data["save_text"]
        self.display_type = data["display_type"]
        self.is_recurring_subscription = data["is_recurring_subscription"]
        self.subs = [Sub(data=sub) for sub in data["subs"]] if data["subs"] else None

class Platforms:
    def __init__(self, *, data):
        self.windows = data["windows"]
        self.mac = data["mac"]
        self.linux = data["linux"]

class Metacritic:
    def __init__(self, *, data):
        self.score = data["score"]
        self.url = data["url"]

class Category:
    def __init__(self, *, data):
        self.id = data["id"]
        self.description = data["description"]

class Genre:
    def __init__(self, *, data):
        self.id = data["id"]
        self.description = data["description"]

class Screenshot:
    def __init__(self, *, data):
        self.id = data["id"]
        self.path_thumbnail = data["path_thumbnail"]
        self.path_full = data["path_full"]

class MovieVideo():
    def __init__(self, *, data):
        self.p480 = data["480"]
        self.max = data["max"]


class Movie:
    def __init__(self, *, data):
        self.id = data["id"]
        self.name = data["name"]
        self.thumbnail = data["thumbnail"]
        self.webm = MovieVideo(data=data["webm"])
        self.mp4 = MovieVideo(data=data["mp4"])
        self.highlight = data["highlight"]

class Recommendations:
    def __init__(self, *, data):
        self.total = data["total"]

class HighlightedAchievement:
    def __init__(self, *, data):
        self.name = data["name"]
        self.path = data["path"]

class Achievements:
    def __init__(self, *, data):
        self.total = data["total"]
        self.highlighted = [HighlightedAchievement(data=highlighted) for highlighted in data["highlighted"]]

class ReleaseDate:
    def __init__(self, *, data):
        self.coming_soon = data["coming_soon"]
        self.date = data["date"]

class SupportInfo:
    def __init__(self, *, data):
        self.url = data["url"]
        self.email = data["email"]

class ContentDescriptors:
    def __init__(self, *, data):
        self.ids = data["ids"]
        self.notes = data["notes"]

class App:
    def __init__(self, *, data):
        self.type = data["type"]
        self.name = data["name"]
        self.steam_appid = data["steam_appid"]
        self.required_age = data["required_age"]
        self.is_free = data["is_free"]
        self.dlc = data["dlc"] if "dlc" in data else None
        self.detailed_description = data["detailed_description"]
        self.about_the_game = data["about_the_game"]
        self.short_description = data["short_description"]
        self.fullgame = data["fullgame"] if "fullgame" in data else None
        self.supported_languages = data["supported_languages"]
        self.reviews = data["reviews"] if "reviews" in data else None
        self.header_image = data["header_image"]
        self.website = data["website"]
        self.pc_requirements = PcRequirements(data=data["pc_requirements"])
        self.mac_requirements = MacRequirements(data=data["mac_requirements"])
        self.linux_requirements = LinuxRequirements(data=data["linux_requirements"])
        self.legal_notice  = data["legal_notice"] if "legal_notice" in data else None
        self.developers = data["developers"] if "developers" in data else None
        self.publishers = data["publishers"]
        self.demos = [Demo(data=demo) for demo in data["demos"]] if "demos" in data else None
        self.price_overview = PriceOverview(data=data["price_overview"]) if "price_overview" in data else None
        self.packages = data["packages"]
        self.package_groups = [PackageGroups(data=package_group) for package_group in data["package_groups"]]
        self.platforms = Platforms(data=data["platforms"])
        self.metacritic = Metacritic(data=data["metacritic"]) if "metacritic" in data else None
        self.categories = [Category(data=category) for category in data["categories"]] if "categories" in data else None
        self.genres = [Genre(data=genre) for genre in data["genres"]] if "genres" in data else None
        self.screenshots = [Screenshot(data=screenshot) for screenshot in data["screenshots"]] if "screenshots" in data else None
        self.movies = [Movie(data=movie) for movie in data["movies"]] if "movies" in data else None
        self.recommendations = Recommendations(data=data["recommendations"]) if "recommendations" in data else None
        self.achievements = Achievements(data=data["achievements"]) if "achievements" in data else None
        self.release_date = ReleaseDate(data=data["release_date"])
        self.support_info = SupportInfo(data=data["support_info"])
        self.background = data["background"]
        self.content_descriptors = ContentDescriptors(data=data["content_descriptors"])
