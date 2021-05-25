from django.shortcuts import render

# Create your views here.

def compare(request):
    topic_list = ['Agriculture & Rural Development','Aid Effectiveness', 'Education',
                  'Economy & Growth','Energy & Mining','Environment','Financial Sector',
                  'Health','Infrastructure','Social Protection & Labor','Poverty',
                  'Private Sector','Public Sector','Science & Technology',
                  'Social Development','Urban Development','Gender','Millenium development goals',
                  'External Debt','Trade']
    topic_list_lower = map(lambda x:x.lower(), topic_list)
    if request.method == 'GET':
        try:
            topic = request.GET['choose_topic']
            if topic.lower() in topic_list_lower:
                context={'topic':topic}
            else:
                context={"error": "Invalid topic"}
        except:
            context = {"error": "Unexpected error"}
    return render(request, 'compare_data/compare.html', context)

def compare_choose_topic(request):
    return render(request, 'compare_data/compare_choose_topic.html')