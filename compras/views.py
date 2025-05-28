# Bibliotecas padrão
import json
from decimal import Decimal
from datetime import datetime

# Bibliotecas de terceiros (Django)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Importações locais (do meu projeto)
from .models import Fornecedor, Compras
from project.utils import generate_success_url
from project.mixins import TenantQuerysetMixin, HandleNoPermissionMixin


@csrf_protect
# Usado para atualizar (POST) os dados em massa da tabela de compras
def compras_update_em_massa(request):
    def parse_date(val):
        if val:
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except Exception:
                return None
        return None

    def parse_decimal(val):
        try:
            return Decimal(str(val)) if val not in [None, ""] else None
        except Exception:
            return None

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        updated_ids = []

        for row in data:
            if not row.get('id'):
                continue

            try:
                compra = Compras.objects.get(pk=row['id'])

                # Datas
                compra.data_compra = parse_date(row.get('data_compra'))
                compra.data_vencimento = parse_date(row.get('data_vencimento'))
                compra.data_pagamento = parse_date(row.get('data_pagamento'))

                # Valores decimais
                compra.valor_compra = parse_decimal(row.get('valor_compra'))
                compra.valor_pago = parse_decimal(row.get('valor_pago'))

                # Campos textuais com default
                text_fields = [
                    'numero_boleto', 'classificacao', 'forma_pagamento',
                    'qtd', 'observacao', 'grupo_produto', 'produto'
                ]
                for field in text_fields:
                    setattr(compra, field, row.get(field, ""))

                # Fornecedor
                try:
                    compra.fornecedor = Fornecedor.objects.get(pk=row['fornecedor']) if row.get('fornecedor') else None
                except Fornecedor.DoesNotExist:
                    compra.fornecedor = None

                compra.save()
                updated_ids.append(compra.id)

            except Compras.DoesNotExist:
                continue

        return JsonResponse({
            "status": "success",
            "updated_count": len(updated_ids),
            "updated_ids": updated_ids
        })

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


class FornecedorListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedor_list.html'  # Garante que o template correto será usado
    permission_required = 'compras.view_fornecedor'  # Permissão para visualizar objetos'

    def get_queryset(self):
        # Obtém o tenant do usuário logado
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return Fornecedor.objects.none()  # Retorna vazio se o tenant não for encontrado

        # Filtra os fornecedores pelo tenant
        queryset = Fornecedor.objects.filter(tenant=tenant)

        # Captura os parâmetros da requisição GET
        nome_empresa = self.request.GET.getlist('nome_empresa[]')

        # Aplica o filtro de nome_empresa apenas se houver valores válidos
        nome_empresa = [nome for nome in nome_empresa if nome.strip()]  # Remove valores vazios e espaços
        if nome_empresa:
            queryset = queryset.filter(nome_empresa__in=nome_empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')  # Converte para minúsculas e substitui espaços por underscores
        context['tenant'] = tenant

        #Filtrar os fornecedores com base no tenant
        context['fornecedores'] = Fornecedor.objects.filter(tenant=self.request.user.tenant)
        # context['numero_boleto'] = Compras.objects.values_list('numero_boleto', flat=True).distinct()
        context['numero_boleto'] = Compras.objects.filter(tenant=self.request.user.tenant).values_list('numero_boleto', flat=True).distinct()

        return context
    

class FornecedorCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Fornecedor
    # campos que o usuario precisa preencher
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    # após o salvamentos redireciona para a view vendas
    success_url = reverse_lazy("fornecedor_list")
    permission_required = 'compras.add_fornecedor'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente
        tenant = getattr(self.request.user, 'tenant', None)  # Busca o tenant associado ao usuário
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # get_success_url é um método que retorna a URL de sucesso após a operação
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('fornecedor_list', tenant)


class FornecedorUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Fornecedor
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    success_url = reverse_lazy("fornecedor_list")
    permission_required = 'compras.change_fornecedor'  # Permissão para visualizar objetos'

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('fornecedor_list', tenant)


class ComprasListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    def compras_list(request):
        if not request.tenant:
            return render(request, 'error.html', {"message": "Tenant not found"})

    model = Compras
    permission_required = 'compras.view_compras'  # Permissão para visualizar objetos'

    def get_queryset(self):
        # Obtém o tenant do usuário logado
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return Compras.objects.none()  # Retorna vazio se o tenant não for encontrado
    
        # Filtra as compras pelo tenant
        queryset = Compras.objects.filter(tenant=tenant).order_by('data_compra')

        # Captura os parâmetros da requisição GET
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        fornecedor_selecionado = self.request.GET.getlist('fornecedor[]')
        boleto_selecionado = self.request.GET.getlist('numero_boleto[]')
        filtro_data = self.request.GET.get('filtro_data', 'compra')  # Padrão é 'compra'

        # Aplica o filtro de datas conforme o radio selecionado
        if data_inicio:
            if filtro_data == 'vencimento':
                queryset = queryset.filter(data_vencimento__gte=data_inicio)
            elif filtro_data == 'pagamento':
                queryset = queryset.filter(data_pagamento__gte=data_inicio)
            else:
                queryset = queryset.filter(data_compra__gte=data_inicio)
        if data_fim:
            if filtro_data == 'vencimento':
                queryset = queryset.filter(data_vencimento__lte=data_fim)
            elif filtro_data == 'pagamento':
                queryset = queryset.filter(data_pagamento__lte=data_fim)
            else:
                queryset = queryset.filter(data_compra__lte=data_fim)

        # Aplica o filtro de fornecedor apenas se houver fornecedores selecionados e ignora valores vazios
        fornecedor_selecionado = [f for f in fornecedor_selecionado if f]  # Remove valores vazios
        if fornecedor_selecionado:  # Só aplica o filtro se a lista não estiver vazia
            queryset = queryset.filter(fornecedor__id__in=fornecedor_selecionado)

        boleto_selecionado = [b for b in boleto_selecionado if b]  # Remove valores vazios
        if boleto_selecionado:
            # boleto_selecionado = [b for b in boleto_selecionado if b and b != "None"]
            queryset = queryset.filter(numero_boleto__in=boleto_selecionado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')
        context['tenant'] = tenant


        # Paginando os resultados
        compras = context['object_list']  # Lista de vendas do queryset
        paginator = Paginator(compras, 10)  # 10 itens por página
        page_number = self.request.GET.get('page')  # Número da página atual
        compras_page = paginator.get_page(page_number)

        context['compras_list'] = compras_page  # Lista paginada para o template
        
        # Filtra os fornecedores e boletos pelo tenant
        context['fornecedores'] = Fornecedor.objects.filter(tenant=self.request.user.tenant)
        context['numero_boleto'] = Compras.objects.filter(tenant=self.request.user.tenant).values_list('numero_boleto', flat=True).distinct()

        # Aqui você monta o JSON para a grid
        # Usado para popular a grid com os dados em massa da tabela de compras
        # compras_queryset = self.get_queryset()
        compras_grid_data = [
            {
                "id": c.pk,
                "data_compra": c.data_compra.strftime('%Y-%m-%d') if c.data_compra else "",
                "data_vencimento": c.data_vencimento.strftime('%Y-%m-%d') if c.data_vencimento else "",
                "data_pagamento": c.data_pagamento.strftime('%Y-%m-%d') if c.data_pagamento else "",
                "fornecedor": c.fornecedor_id, # ID para salvar
                "nome_empresa": c.fornecedor.nome_empresa if c.fornecedor else "",
                "valor_compra": float(c.valor_compra or 0),
                "valor_pago": float(c.valor_pago or 0),
                "numero_boleto": c.numero_boleto or "",
                "grupo_produto": c.grupo_produto,
                "produto": c.produto,
                "classificacao": str(c.classificacao or ""),
                "forma_pagamento": str(c.forma_pagamento or ""),
                "qtd": c.qtd or "",
                "observacao": c.observacao or "",
            }
            # for c in compras_queryset
            for c in compras_page  # Use apenas os itens da página atual
        ]
        context['compras_grid_data_json'] = json.dumps(compras_grid_data, cls=DjangoJSONEncoder)

        return context


class ComprasCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Compras
    # campos que o usuario precisa preencher
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")
    permission_required = 'compras.add_compras'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente
        tenant = getattr(self.request.user, 'tenant', None)  # Busca o tenant associado ao usuário
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Filtra os fornecedores pelo tenant no formulário de criação
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # Filtra os fornecedores pelo tenant
            form.fields['fornecedor'].queryset = Fornecedor.objects.filter(tenant=tenant)
        return form

    # get_success_url é um método que retorna a URL de sucesso após a operação
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('compras_list', tenant)


class ComprasUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Compras
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")
    permission_required = 'socio.change_compras'  # Permissão para visualizar objetos'

    # Filtra os fornecedores pelo tenant no formulário de criação
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # Filtra os fornecedores pelo tenant
            form.fields['fornecedor'].queryset = Fornecedor.objects.filter(tenant=tenant)
        return form

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('compras_list', tenant)
    

class ComprasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, DeleteView):
    model = Compras
    success_url = reverse_lazy("compras_list")
    permission_required = 'socio.delete_compras'  # Permissão para visualizar objetos'

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('compras_list', tenant)