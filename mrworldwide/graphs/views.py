from django.shortcuts import render
from datetime import datetime
from apis.worldbank import get_indicator_code, get_indicator_names, get_indicator_definition
from apis.graphs import graph_1dataXcountries, graph_Xdata1country, graph_histograma
from apis.restcountries import get_all_names, get_iso3code
import base64
import os
import traceback

# Create your views here.

indicators = get_indicator_names()
indicator_list = [indicators[indicator] for indicator in indicators]
country_list = get_all_names()

def get_indicators_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path,"indicators.csv")

def graphs_index(request):
    return render(request, 'graphs/graph_index.html')

# Para las siguientes 3 vistas solo se pasa como contexto la lista
# de indicadores y de países para que se autocompleten los formularios

def graphs_1dataXcountries(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_1dataXcountries.html', context)

def graphs_Xdata1country(request):
    context = {'indicator_list':indicator_list, 'country_list':country_list}
    return render(request, 'graphs/graph_Xdata1country.html', context)

def graphs_histogram(request):
    context = {'indicator_list':indicator_list}
    return render(request, 'graphs/graph_histogram.html', context)

# Vista que gestiona el resultado del CU del histograma
def graphs_histogram_result(request):
    if request.method == 'GET':
        try:
            # Prueba a sacar el formulario del indicador
            indicator = request.GET['graph_indicator1']
            icode = get_indicator_code(indicator)
            inddef = get_indicator_definition(icode)
            try:
                # Generamos el nombre del fichero para guardar el gráfico combinando la IP de origen del cliente con el timestamp de la petición
                # De esta manera nos aseguramos de que no se repiten los nombres de ficheros
                nombre_fichero = get_indicators_path() + str(request.META['REMOTE_ADDR']).replace(".", "-") + "-" + str(datetime.now().timestamp()).replace(".", "") + ".jpg"
                graph_histograma(icode, filename=nombre_fichero)
                with open(nombre_fichero, "rb") as f:
                    content = f.read()
                    encoded_img = base64.b64encode(content).decode(encoding="utf-8")
                    os.remove(f.name)
                context={'indicator':indicator, 'graph':encoded_img, 'def':inddef}
            except:
                context={"error": "There was an error doing graph"}
        except:
            context={"error": "Invalid indicator"}
    return render(request, 'graphs/graph_histogram_result.html', context)

# Vista que gestiona el resultado del CU de comparar un indicador
# sobre varios países
def graphs_1dataXcountries_result(request):
    if request.method == 'GET':
        try:
            # Prueba a sacar el formulario del indicador
            indicator = request.GET['graph_indicator1']
            icode = get_indicator_code(indicator)
            inddef = get_indicator_definition(icode)
            try:
                # Prueba a sacar los formularios de los países obligatorios y luego comprueba los opcionales
                country1 = request.GET['graph_country1']
                countries = [get_iso3code(country1)]
                if (request.GET['graph_country2']):
                    country2 = request.GET['graph_country2']
                    countries.append(get_iso3code(country2))
                if (request.GET['graph_country3']):
                    country3 = request.GET['graph_country3']
                    countries.append(get_iso3code(country3))
                if (request.GET['graph_country4']):
                    country4 = request.GET['graph_country4']
                    countries.append(get_iso3code(country4))
                if (request.GET['graph_country5']):
                    country5 = request.GET['graph_country5']
                    countries.append(get_iso3code(country5))
                # Si el usuario escoge países repetidos se eliminan para aligerar la petición
                countries = list(dict.fromkeys(countries))
                try:
                    # Generamos el nombre del fichero para guardar el gráfico combinando la IP de origen del cliente con el timestamp de la petición
                    # De esta manera nos aseguramos de que no se repiten los nombres de ficheros
                    nombre_fichero = get_indicators_path() + str(request.META['REMOTE_ADDR']).replace(".", "-") + "-" + str(datetime.now().timestamp()).replace(".", "") + ".jpg"
                    graph_1dataXcountries(icode, countries, filename=nombre_fichero)
                    with open(nombre_fichero, "rb") as f:
                        content = f.read()
                        encoded_img = base64.b64encode(content).decode(encoding="utf-8")
                        os.remove(f.name)
                    context={'indicator':indicator, 'graph':encoded_img, 'def':inddef}
                except:
                    context={"error": "There was an error doing graph"}
            except:
                context={"error": "Invalid country"}
        except:
            context={"error": "Invalid indicator"}
    return render(request, 'graphs/graph_1dataXcountries_result.html', context)

# Vista que gestiona el resultado del CU de comparar varios indicadores
# sobre un país
def graphs_Xdata1country_result(request):
    if request.method == 'GET':
        try:
            # Prueba a sacar el formulario del país
            country = request.GET['graph_country1']
            ccode = get_iso3code(country)
            try:
                # Prueba a sacar los formularios de los indicadores obligatorios y luego comprueba los opcionales
                indicator1 = request.GET['graph_indicator1']
                indicators = [get_indicator_code(indicator1)]
                if (request.GET['graph_indicator2']):
                    indicator2 = request.GET['graph_indicator2']
                    indicators.append(get_indicator_code(indicator2))
                if (request.GET['graph_indicator3']):
                    indicator3 = request.GET['graph_indicator3']
                    indicators.append(get_indicator_code(indicator3))
                if (request.GET['graph_indicator4']):
                    indicator4 = request.GET['graph_indicator4']
                    indicators.append(get_indicator_code(indicator4))
                if (request.GET['graph_indicator5']):
                    indicator5 = request.GET['graph_indicator5']
                    indicators.append(get_indicator_code(indicator5))
                # Si el usuario escoge indicadores repetidos se eliminan para aligerar la petición
                # y tras esto se aplica a la lista resultante la funcion para conseguir sus descripciones
                indicators = list(dict.fromkeys(indicators))
                inddef_list = map(get_indicator_definition, indicators)
                try:
                    # Generamos el nombre del fichero para guardar el gráfico combinando la IP de origen del cliente con el timestamp de la petición
                    # De esta manera nos aseguramos de que no se repiten los nombres de ficheros
                    nombre_fichero = get_indicators_path() + str(request.META['REMOTE_ADDR']).replace(".", "-") + "-" + str(datetime.now().timestamp()).replace(".", "") + ".jpg"
                    graph_Xdata1country(indicators, ccode, filename=nombre_fichero)
                    with open(nombre_fichero, "rb") as f:
                        content = f.read()
                        encoded_img = base64.b64encode(content).decode(encoding="utf-8")
                        os.remove(f.name)
                    context={'country':country, 'graph':encoded_img, 'def':inddef_list}
                except:
                    context={"error": "There was an error doing graph"}
            except:
                context={"error": "Invalid indicator"}
        except:
            context={"error": "Invalid country"}
    return render(request, 'graphs/graph_Xdata1country_result.html', context)