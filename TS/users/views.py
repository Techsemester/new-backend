from django.shortcuts import render

def home(request):
    # greet = "SpendWise!"
    # slogan = "... Take Control, Achieve!"
    if request.method == 'POST':
        print(request.POST)
    else:
        getting = "We are home!"
        print(getting)
        resp = render(request, 'account/home.html')

        # set http response header and value. For browser caching
        resp['Cache-Control'] = 'public,max-age=3600'
        resp['Vary'] = 'Accept-Encoding'

        return resp
