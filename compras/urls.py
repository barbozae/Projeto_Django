from django.urls import path
from compras.views import FornecedorListView, FornecedorCreateView, FornecedorUpDateView, ComprasListView, ComprasCreateView, ComprasUpDateView, ComprasDeleteView


urlpatterns = [
                # Rotas para fornecedores
                path('fornecedores/', FornecedorListView.as_view(), name="fornecedor_list"),
                path('create_fornecedor/', FornecedorCreateView.as_view(), name="create_fornecedor"),
                path('update_fornecedor/<int:pk>', FornecedorUpDateView.as_view(), name="update_fornecedor"),

                # Rotas para compras
                path('compras/', ComprasListView.as_view(), name="compras_list"),
                path('create_compras/', ComprasCreateView.as_view(), name="create_compras"),
                path('update_compras/<int:pk>', ComprasUpDateView.as_view(), name="update_compras"),
                path('delete_compras/<int:pk>', ComprasDeleteView.as_view(), name='delete_compras'),
            ]