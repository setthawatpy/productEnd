from django.urls import path
from product import views


urlpatterns = [
    # Category
    path('createCategory', views.createCategory, name='createCategory'),
    path('editCategory/<int:id>', views.editCategory, name='editCategory'),
    path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('categoryList', views.categoryList, name='categoryList'),
    path('search_category', views.search_category, name='search_category'),
    
    # Product
    path('createProduct', views.createProduct, name='createProduct'),
    path('editProduct/<id>', views.editProduct, name='editProduct'),
    path('deleteProduct/<id>', views.deleteProduct, name='deleteProduct'),
    path('productList', views.productList, name='productList'),
    path('productDetail/<id>', views.productDetail, name='productDetail'),
    path('search_product', views.search_product, name='search_product'),
    
    # Show Product
    path('category', views.category, name='category'),
    path('goldBangle', views.goldBangle, name='goldBangle'),
    path('goldBars', views.goldBars, name='goldBars'),
    path('goldBracelet', views.goldBracelet, name='goldBracelet'),
    path('goldEarrings', views.goldEarrings, name='goldEarrings'),
    path('goldNecklace', views.goldNecklace, name='goldNecklace'),
    path('goldRing', views.goldRing, name='goldRing'),
]
