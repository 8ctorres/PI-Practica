from django.shortcuts import render
from jsonschema import validate, ValidationError
from numpy import iscomplexobj
from .schemas import topn_schema
from apis.worldbank import get_indicator_names,get_indicator_code
from apis.graphs import graph_topn
from apis.restcountries import get_name_from_iso3
from apis.exceptions import APIRequestException
import os
from uuid import uuid4
import base64
from .exceptions import TopAmountExceeded
import traceback

def top(request):
    indicators = get_indicator_names()
    indicators_names = [indicators[indicator] for indicator in indicators]
    if request.method == 'GET':
        context = {"indicators": indicators_names}
        return render(request, 'top_countries/top.html',context)
    elif request.method == 'POST':
        try:
            # Validate post data
            validate(instance=request.POST, schema=topn_schema)
            queryDict = request.POST.dict()
            unpackedBody = [ queryDict[key] for key in ["indicator","top"] ]
            indicator,top = unpackedBody
            top = int(top)
            indicator_code = get_indicator_code(indicator)
            if top > 20:
                raise TopAmountExceeded(top)
            graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{uuid4()}.jpg")            
            graph = graph_topn(indicator_code,top,graph_path)
            isolist = graph.index.to_list()
            namelist = map(get_name_from_iso3, isolist)
            with open(graph_path, "rb") as f:
                content = f.read()
                encoded_img = base64.b64encode(content).decode(encoding="utf-8")
                os.remove(f.name)
            context = {'indicator': indicator, 'top': top, 'graph': encoded_img, 'namelist':namelist}
        except ValidationError:
            context = {"indicators": indicators_names,'error': 'Invalid parameters'}
        except TopAmountExceeded:
            context = {"indicators": indicators_names,'error': f'Maximum amount of countries allowed are 50, {top} requested'}
        except APIRequestException:
            context = {"indicators": indicators_names,'error': 'Server error'}
        except KeyError:
            context = {"indicators": indicators_names,'error': 'Unsupported indicator'}
        except Exception:
            context = {"indicators": indicators_names,'error': 'Unexpected error'}
        return render(request, 'top_countries/top.html', context)