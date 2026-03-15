from .models import Category

def menu_categories(request):
    """
    Returns categories for the global navbar dropdown.
    """
    all_categories = Category.objects.all()
    categories = all_categories[:20]
    has_more = all_categories.count() > 20
    return {
        "menu_categories": categories,
        "has_more_categories": has_more
    }
