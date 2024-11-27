from .models import Category

def category_menu(request):
    """
    Context processor to make all categories globally available.
    """
    categories = Category.objects.all()
    return {'categories': categories}
