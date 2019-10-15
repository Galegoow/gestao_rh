from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apps.core.serializers import UserSerializer, GroupSerializer
from apps.registro_hora_extra.models import RegistroHoraExtra
from .tasks import send_relatorio

@login_required
def home(request):
    data = {}
    data['usuario'] = request.user
    funcionario = request.user.funcionario
    data['total_funcionarios'] = funcionario.empresa.total_funcionarios or 0
    data['total_funcionarios_ferias'] = funcionario.empresa.total_funcionarios_ferias or 0
    data['total_funcionarios_doc_pendente'] = funcionario.empresa.total_funcionarios_doc_pendente or 0
    data['total_funcionarios_doc_ok'] = funcionario.empresa.total_funcionarios_doc_ok or 0
    data['total_hora_extra_utilizadas'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=True).aggregate(Sum('horas'))['horas__sum'] or 0
    data['total_hora_extra_pendente'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=False).aggregate(Sum('horas'))['horas__sum'] or 0

    return render(request, 'core/index.html', data)


def celery(request):
    send_relatorio.delay()
    return HttpResponse('Tarefa incluida na fila para execucao')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer