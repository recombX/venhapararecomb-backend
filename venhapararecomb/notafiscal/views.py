from django.shortcuts import render
import xml.etree.ElementTree as et


def index(request):
    if request.method == 'POST':
        
        print('entrou')
        xml_file = request.FILES['xml_file']
        tree = et.parse(xml_file)
        root = tree.getroot()
        print(root)
        for element in root:
            print(element.tag)
    
    return render(request, 'index.html')