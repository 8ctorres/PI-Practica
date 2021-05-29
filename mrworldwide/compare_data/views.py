from django.shortcuts import render
from apis.restcountries import get_countries_by_name
#from apis.worldbank import *
from apis.exceptions import APIRequestException

# Create your views here.

topic_indicator = {
    'Health':['Mortality rate under 5, per 1.000 births',
        'Incidence of tuberculosis per 100.000 people',
        'Population ages 15-49 with HIV(%)',
        'Life expectancy',
        'Fertility rate(births per woman)'],
    'Economy':['GDP(PIB)',
        'GNI',
        'Total trade(% of GPD)',
        'Trade in services(% of GDP)',
        'Merchandise trade(% of GDP)',
        'Exports of goods and services($)',
        'High-technology exports($)',
        'Research and development expenditure(% of GPD)',
        'Exports of goods, services & primary income',
        'GDP % of industry',
        'Industry value in $',
        'Total reserves',
        'GDP % of Agriculture, forestry and fishing',
        'Pump price for gasoline $/L',
        'High-technology exports($)',
        'Total natural resources rents % of GDP(minerals, oil, natural gas...)'], 
    'Enviroment':['CO2 emissions (kt)',
        'CO2 emissions from gaseous fuel(% of total)',
        'Bird species threatened',
        'Plant species threatened',
        'Mammal species thretened',
        'Protected areas(% of total area)',
        'Agricultural land',
        'Forest area'],
    'Social Development':['Population',
        'Population growth(annual %)',
        'Population density(people/km2)',
        'Urban population',
        'Urban population grownth(annual %)',
        'Urban population %(of total)',
        'Rural population',
        'Access to electricity % of population',
        'Percentage of population ages 0-14',
        'Percentage of unemployment',
        'People employed or seeking work',
        'Adolescents out of school',
        'Refugees by country',
        'Proportion of seats held by women in national parliaments(%)',
        'Percentage of population using internet',
        'Vulnerable employment',
        'Employment in service(% of total)',
        'Percentage of unemployment']}

def compare(request):
    topic_list = topic_indicator.keys()
    topic_list_lower = map(lambda x:x.lower(), topic_list)
    if request.method == 'GET':
        try:
            topic = request.GET['choose_topic']
            if topic.lower() in topic_list_lower:
                context={'topic':topic, 'topic_list':topic_list,'health_list':topic_indicator['Health'],
                         'economy_list':topic_indicator['Economy'], 'enviroment_list':topic_indicator['Enviroment'],
                         'social_development_list':topic_indicator['Social Development'],}
            else:
                context={"error": "Invalid topic"}
        except:
            context = {"error": "Unexpected error"}
    return render(request, 'compare_data/compare.html', context)

def compare_choose_topic(request):
    return render(request, 'compare_data/compare_choose_topic.html')

def compare_result(request):
    if request.method == 'GET':
        try:
            country1 = request.GET['compare_country1']
            country2 = request.GET['compare_country2']
            try:
                indicator = request.GET['compare_indicator']
                
                context={'country1':country1, 'country2':country2, 'indicator':indicator}
            except:
                context={"error": "Invalid indicator"}
        except:
                context={"error": "Invalid country"}
    return render(request, 'compare_data/compare_result.html', context)