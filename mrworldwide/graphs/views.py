from django.shortcuts import render
from datetime import datetime
from apis.worldbank import get_indicator_code, get_indicator_names
from apis.graphs import graph_1dataXcountries, graph_Xdata1country, graph_histograma
from apis.restcountries import get_all_names, get_iso3code
import base64
import os
import traceback

# Create your views here.

indicators = get_indicator_names()
indicator_list = [indicators[indicator] for indicator in indicators]
country_list = get_all_names()

def graphs_index(request):
    return render(request, 'graphs/graph_index.html')

def graphs_1dataXcountries(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_1dataXcountries.html', context)

def graphs_Xdata1country(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_Xdata1country.html', context)

def graphs_histogram(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_histogram.html', context)

def graphs_histogram_result(request):
    return render(request, 'graphs/graph_histogram_result.html')

def graphs_1dataXcountries_result(request):
    if request.method == 'GET':
        try:
            # Prueba a sacar el formulario del indicador
            indicator = request.GET['graph_indicator1']
            try:
                # Prueba a sacar los formularios de los países obligatorios
                country1 = request.GET['graph_country1']
                country2 = request.GET['graph_country2']
                countries = [get_iso3code(country1), get_iso3code(country2)]
                if (request.GET['graph_country3']):
                    country3 = request.GET['graph_country3']
                    countries.append(get_iso3code(country3))
                if (request.GET['graph_country4']):
                    country4 = request.GET['graph_country4']
                    countries.append(get_iso3code(country4))
                if (request.GET['graph_country5']):
                    country5 = request.GET['graph_country5']
                    countries.append(get_iso3code(country5))
                try:
                    # Generamos el nombre del fichero para guardar el gráfico combinando la IP de origen del cliente con el timestamp de la petición
                    # De esta manera nos aseguramos de que no se repiten los nombres de ficheros
                    nombre_fichero = "./graphs/temp/" + str(request.META['REMOTE_ADDR']).replace(".", "-") + "-" + str(datetime.now().timestamp()).replace(".", "") + ".jpg"
                    graph_1dataXcountries(get_indicator_code(indicator), countries, filename=nombre_fichero)
                    with open(nombre_fichero, "rb") as f:
                        content = f.read()
                        encoded_img = base64.b64encode(content).decode(encoding="utf-8")
                        os.remove(f.name)
                    context={'indicator':indicator, 'graph':encoded_img}
                except:
                    traceback.print_exc()
                    context={"error": "There was an error doing graph"}
            except:
                context={"respuesta": "Invalid country"}
        except:
            context={"error": "Invalid indicator"}
    return render(request, 'graphs/graph_1dataXcountries_result.html', context)

def graphs_Xdata1country_result(request):
    return render(request, 'graphs/graph_Xdata1country_result.html')