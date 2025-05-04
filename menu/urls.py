from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
# from menu.views import MenuListView
from .views import menu_view

# urlpatterns = [
#                 path('menu/', MenuListView.as_view(), name="menu"),
#                 path('create_payment/', MenuCreateView.as_view(), name="create_payment"),
#                 path('update_payment/<int:pk>', MenuUpDateView.as_view(), name="update_payment"),
#                 path('delete_payment/<int:pk>', MenuDeleteView.as_view(), name="delete_payment"),
#             ]

urlpatterns = [
    path('menu/', menu_view, name='menu'),
]


# urlpatterns = [
#     path('', menu_view, name='menu'),  # Acessível em /menu/?tenant=<nome_do_tenant>
# ]


# urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)