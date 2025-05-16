from django.urls import get_resolver, reverse, NoReverseMatch
from seller_app.models import Seller  # Adjust the import based on your app name

def list_all_urls():
    url_patterns = get_resolver().url_patterns
    url_list = []
    #print(f"DEBUG URL patterns: {url_patterns}")

    def extract_urls(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):  # included patterns
                #print(f"DEBUG URL patterns: {pattern.url_patterns}")
                extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                try:
                    # Try to reverse by name if available
                    name = pattern.name
                    if name:
                        url = reverse(name)
                        url_list.append((name, url))
                except NoReverseMatch:
                    # Skip patterns with arguments or unresolved ones
                    pass
    def add_sellers_to_urls(url_list):
        sellers = Seller.objects.all()
        for seller in sellers:
            try:
                url = reverse('landing_page_per_seller', args=[seller.slug])
                url_list.append((f"landing_page_per_seller_{seller.slug}", url))
                #print(f"DEBUG URL for seller {seller.slug}: {url}")
            except NoReverseMatch:
                pass

    extract_urls(url_patterns)
    return url_list