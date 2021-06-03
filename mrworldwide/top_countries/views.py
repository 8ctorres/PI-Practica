from django.shortcuts import render
from jsonschema import validate, ValidationError
from .schemas import topn_schema
from apis.worldbank import get_indicator_names,get_indicator_code
from apis.graphs import top_n_indicador
from apis.restcountries import get_all_countries
from apis.exceptions import APIRequestException

def top(request):
    if request.method == 'GET':
        indicators = get_indicator_names()
        indicators_names = [indicators[indicator] for indicator in indicators]

        context = {"indicators": indicators_names}
        return render(request, 'top_countries/top.html',context)
    elif request.method == 'POST':
        try:
            # Validate post data
            validate(instance=request.POST, schema=topn_schema)
            queryDict = request.POST.dict()
            unpackedBody = [ queryDict[key] for key in ["indicator","top"] ]
            indicator,top = unpackedBody
            indicator_code = get_indicator_code(indicator)
            serietop = gp.top_n_indicador(indicator_code,5)
            print(serietop)
            context = {'indicator': indicator, 'top': top}
        except ValidationError:
            context = {'error': 'Invalid parameters'}
        except APIRequestException:
            context = {'error': 'Server error'}
        except Exception:
            context = {'error': 'Unexpected error'}
        return render(request, 'top_countries/top.html', context)