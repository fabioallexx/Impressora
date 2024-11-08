import win32print
import win32api
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Leitor
import os
from django.conf import settings
import re

def imprimir_etiqueta(request, numero_leitor):
    leitor = get_object_or_404(Leitor, numero_leitor=numero_leitor)
    zpl_content = gerar_zpl(leitor.numero_leitor, leitor.nome, leitor.apelido)

    try:
        enviar_para_impressora(zpl_content)
        return HttpResponse("Etiqueta enviada para impressão com sucesso.")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar a etiqueta para impressão: {e}", status=500)

def imprimir_etiquetas(request):
    if request.method == 'POST':
        input_range = request.POST.get("intervalos")
        numeros_para_imprimir = processar_input(input_range)

        if not numeros_para_imprimir:
            return HttpResponse("Nenhum número válido foi fornecido.", status=400)

        request.session['numeros_para_imprimir'] = numeros_para_imprimir

        return render(request, 'Imprimir/visualizar_impressao.html', {
            'numeros': numeros_para_imprimir
        })
    
    return render(request, 'Imprimir/imprimir_intervalos.html')

def visualizar_impressao(request):
    """
    Função para exibir os números que foram selecionados para impressão
    """
    numeros_para_imprimir = request.session.get('numeros_para_imprimir', [])

    if not numeros_para_imprimir:
        return HttpResponse("Nenhum número para visualizar.", status=400)

    return render(request, 'Imprimir/visualizar_impressao.html', {
        'numeros': numeros_para_imprimir
    })

def processar_input(input_range):
    """
    Função para processar os intervalos de números e números individuais inseridos pelo usuário.
    A entrada pode ser um intervalo (ex: 75-89) ou números individuais separados por vírgulas (ex: 75, 91, 103).
    """
    numeros = set()
    
    pattern = re.compile(r'(\d+)-(\d+)|(\d+)')
    matches = pattern.findall(input_range)
    
    for match in matches:
        if match[0] and match[1]:
            start, end = int(match[0]), int(match[1])
            for num in range(start, end + 1):
                numeros.add(num)
        elif match[2]:
            numeros.add(int(match[2]))

    return sorted(numeros)

def enviar_para_impressora(zpl):
    printer_name = "ZDesigner GK420t (EPL)"
    try:
        printer_handle = win32print.OpenPrinter(printer_name)
        job = win32print.StartDocPrinter(printer_handle, 1, ("Etiqueta", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)
        
        win32print.WritePrinter(printer_handle, zpl.encode('utf-8'))
        
        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)
    except Exception as e:
        raise Exception(f"Erro ao enviar ZPL para a impressora: {e}")

def lista_leitores(request):
    leitores = Leitor.objects.all()
    return render(request, 'Imprimir/imprimir_intervalos.html', {'leitores': leitores})

def gerar_zpl(numero_leitor, nome_leitor, apelido_leitor):
    zpl_path = os.path.join(settings.BASE_DIR, "zpl_templates", "biblioteca.zpl")
    with open(zpl_path, "r") as file:
        zpl_template = file.read()

    zpl_template = zpl_template.replace("{CODIGO}", str(numero_leitor))
    zpl_template = zpl_template.replace("{Nome}", nome_leitor)
    zpl_template = zpl_template.replace("{Apelidos}", apelido_leitor)

    return zpl_template

def visualizar_etiqueta(request, numero_leitor):
    leitor = get_object_or_404(Leitor, numero_leitor=numero_leitor)

    if request.method == "POST" and request.POST.get("action") == "confirmar":
        zpl_content = gerar_zpl(leitor.numero_leitor, leitor.nome, leitor.apelido)

        try:
            enviar_para_impressora(zpl_content)
            return HttpResponse("Etiqueta enviada para impressão com sucesso.")
        except Exception as e:
            return HttpResponse(f"Erro ao enviar a etiqueta para impressão: {e}", status=500)
    
    return render(request, 'Imprimir/visualizar_etiqueta.html', {'leitor': leitor})

def confirmar_impressao(request):
    numeros_para_imprimir = request.session.get('numeros_para_imprimir', [])

    if not numeros_para_imprimir:
        return HttpResponse("Nenhum número para imprimir.", status=400)

    for numero in numeros_para_imprimir:
        try:
            leitor = get_object_or_404(Leitor, numero_leitor=numero)
            zpl_content = gerar_zpl(leitor.numero_leitor, leitor.nome, leitor.apelido)
            enviar_para_impressora(zpl_content)
        except Exception as e:
            return HttpResponse(f"Erro ao enviar a etiqueta para o número {numero}: {e}", status=500)

    del request.session['numeros_para_imprimir']

    return HttpResponse("Etiquetas enviadas para impressão com sucesso.")

def remover_numero(request, numero):
    numeros_para_imprimir = request.session.get('numeros_para_imprimir', [])

    if numero in numeros_para_imprimir:
        numeros_para_imprimir.remove(numero)
        request.session['numeros_para_imprimir'] = numeros_para_imprimir

    return render(request, 'Imprimir/visualizar_impressao.html', {
        'numeros': numeros_para_imprimir
    })