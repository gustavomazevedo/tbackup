# Create your views here.

from django.shortcuts import render_to_response

def get_config_file(request,machine_id):
    if request.method == GET:
        return render_to_response('transfer/index.html')

def post_log(request, machine_hash):
    if request.method == POST:
        return render_to_response('transfer/index.html')
    
