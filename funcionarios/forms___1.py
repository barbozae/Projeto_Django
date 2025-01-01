from django import forms

from .models import Contratacao


class ContratacaoForm(forms.ModelForm):
    nome_funcionario = forms.ModelChoiceField(
        queryset=Contratacao.objects.all(),
        empty_label="Selecione um Funcionário",
        to_field_name="nome"  # Isso garante que o nome do funcionário seja exibido
    )

    class Meta:
        model = Contratacao
        fields = ["nome_funcionario", "cargo", "setor", "data_exame_admissional", "data_contratacao", "salario",
                  "documentacao_admissional", "contabilidade_admissional", "observacao_admissional"]