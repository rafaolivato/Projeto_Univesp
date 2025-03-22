from django import forms
from localflavor.br.forms import BRCPFField
from .models import Paciente, Endereco

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
    
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        return nome.upper()

class PacienteForm(forms.ModelForm):
    cpf = BRCPFField()
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    endereco = EnderecoForm() # instancia o form de endereço.

    class Meta:
        model = Paciente
        fields = ['nome', 'cnes', 'cpf', 'data_nascimento', 'telefone']

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        return nome.upper()

    def save(self, commit=True):
        endereco_form = EnderecoForm(self.data)  # Cria uma instância do EnderecoForm com os dados do request
        if endereco_form.is_valid():
            endereco_obj = endereco_form.save() # Salva o endereço.
            paciente = super().save(commit=False)
            paciente.endereco = endereco_obj
            if commit:
                paciente.save()
            return paciente
        else:
            raise ValueError("Formulário de endereço inválido") # Lança um erro caso o form de endereço seja invalido.
        
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    

    class Meta:
        model = Produto
        fields = '__all__'

from django import forms
from .models import Fabricante

class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = '__all__'

from django import forms
from .models import EntradaEstoque

class EntradaEstoqueForm(forms.ModelForm):
    class Meta:
        model = EntradaEstoque
        fields = '__all__'
        widgets = {
            'validade': forms.DateTimeInput(attrs={'type': 'date'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'


from django import forms
from .models import Dispensacao

class DispensacaoForm(forms.ModelForm):
    class Meta:
        model = Dispensacao
        fields = '__all__'


from django import forms
from .models import SaidaEstoque

class SaidaEstoqueForm(forms.ModelForm):
    class Meta:
        model = SaidaEstoque
        fields = ['produto', 'quantidade', 'motivo']