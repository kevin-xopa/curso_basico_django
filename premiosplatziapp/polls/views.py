from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Estas en la pagina principal nene")


def detail(request, question_id):
    return HttpResponse(f'es la pregunta No. {question_id}')


def results(request, question_id):
    return HttpResponse(f'estos son los resultados de la pregunta No. {question_id}')


def vote(request, question_id):
    return HttpResponse(f'estas votando por la pregunta No. {question_id}')
