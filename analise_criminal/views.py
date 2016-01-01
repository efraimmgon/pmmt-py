from django.shortcuts import render
from django.http import HttpResponse

import json

from setup_app.models import Ocorrencia
from analise_criminal.forms import MapOptionForm, MapMarkerStyleForm
from analise_criminal.functions import format_data


def map(request):
	"""/analise_criminal/mapa/"""
	form_styles = MapMarkerStyleForm()
	form_options = MapOptionForm()
	
	available = {
		'from': Ocorrencia.objects.first(),
		'to': Ocorrencia.objects.last()
	}
	context = {
		'form_options': form_options, 'form_styles': form_styles,
		'availability': available
	}

	return render(request, 'analise_criminal/mapa.html', context)

def mapAjax(request):
	if request.method == 'POST':
		form = MapOptionForm(data=request.POST)
		form.full_clean()
		if form.is_valid():
			natureza = form.cleaned_data['natureza']
			data_inicial = form.cleaned_data['data_inicial']
			data_final = form.cleaned_data['data_final']
			hora_inicial = form.cleaned_data['hora_inicial']
			hora_final = form.cleaned_data['hora_final']
			
			if hora_inicial is None:
				hora_inicial = '00:00'
			if hora_final is None:
				hora_final = '23:59'

			if natureza == 'todas':
				o = Ocorrencia.objects.filter(
					data__gte=data_inicial, data__lte=data_final,
					hora__gte=hora_inicial, hora__lte=hora_final
				)
			else:
				o = Ocorrencia.objects.filter(natureza__contains=natureza, 
					data__gte=data_inicial, data__lte=data_final,
					hora__gte=hora_inicial, hora__lte=hora_final
				)

			json_data = format_data(o)

			return HttpResponse(json_data, content_type='application/json')
		## refactor forms.py to have portuguese errors.
		else:
 	 		data = json.dumps({'errors': form.errors})
 	 		return HttpResponse(data, content_type='application/json')

