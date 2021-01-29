from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from .entidades import clientes
from .services import cliente_service


# Create your views here.

def listar_clientes(request):
    # clientes = Cliente.objects.all() metodo1
    clientes = cliente_service.listar_clientes()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})


def inserir_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            # form.save()
            nome = form.cleaned_data["nome"]
            sexo = form.cleaned_data["sexo"]
            data_nascimento = form.cleaned_data["data_nascimento"]
            email = form.cleaned_data["email"]
            profissao = form.cleaned_data["profissao"]
            cliente_novo = clientes.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email, profissao=profissao)
            cliente_service.cadastrar_cliente(cliente_novo)
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form_cliente.html', {'form': form})


def listar_cliente_id(request, id):
    # cliente = Cliente.objects.get(id=id) metdo1
    cliente = cliente_service.listar_cliente_id(id)

    return render(request, 'clientes/lista_cliente.html', {'cliente': cliente})


def editar_cliente(request, id):
    cliente_antigo = cliente_service.listar_cliente_id(id)
    form = ClienteForm(request.POST or None, instance=cliente_antigo)
    if form.is_valid():
        # form.save()
        nome = form.cleaned_data["nome"]
        sexo = form.cleaned_data["sexo"]
        data_nascimento = form.cleaned_data["data_nascimento"]
        email = form.cleaned_data["email"]
        profissao = form.cleaned_data["profissao"]
        cliente_novo = clientes.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email, profissao=profissao)
        cliente_service.editar_cliente(cliente_antigo, cliente_novo)
        return redirect('listar_clientes')

    return render(request, 'clientes/form_cliente.html', {'form': form})


def excluir_cliente(request, id):
    cliente = cliente_service.listar_cliente_id(id)
    if request.method == "POST":
        #cliente.delete() metodo antigo
        cliente_service.remover_cliente(cliente)
        return redirect('listar_clientes')
    return render(request, 'clientes/confirma_exclusao.html', {'cliente': cliente})
