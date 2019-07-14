from django.shortcuts import render

from .models import IntermineService

#import requests

# Create your views here.
def index(request) :
    """
    # Parse the request content, extract the gene
    gene = request.GET.get('gene')

    # Aggregate the results
    hh = []
    tt = []
    services = LinkoutService.objects.all()
    for service in services :
        try :
            rr = requests.get(service.insert_gene(gene))
            jj = rr.json()
            for j in jj :
                href = j['href']
                # TODO: confirm whether to prepend 'http:'
                if (not href.startswith('http')) :
                    href = 'http:' + href
                hh.append(href)
                tt.append(j['text'])
        except :
            pass

    aggregated_links = zip(hh, tt)
    context = {
        'gene': gene,
        'aggregated_links': aggregated_links,
    }
    """
    context = {
        'url': 'http://www.ncgr.org'
    }
    return render(request, 'intermine_mgr/index.html', context)

