from django.shortcuts import render

from .models import GeneLinkout, GenomicRegionLinkout

import requests

# Create your views here.
def index(request) :
    if not (request.GET.get('gene') == None) :
        context = gene_context(request)
    elif not (request.GET.get('seqname') == None or request.GET.get('start') == None or request.GET.get('end') == None) :
        context = genomic_region_context(request)
    else :
        context = {}
    return render(request, 'linkout_mgr/index.html', context)

def gene_context(request) :
    gene = request.GET.get('gene')

    # Aggregate the results
    hh = []
    tt = []
    services = GeneLinkout.objects.all()
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
        'linkout_type': 'gene',
        'label': gene,
        'aggregated_links': aggregated_links,
    }
    return context

def genomic_region_context(request) :
    sequence_name = request.GET.get('seqname')
    start_pos = request.GET.get('start')
    end_pos = request.GET.get('end')

    # Aggregate the results
    hh = []
    tt = []
    services = GenomicRegionLinkout.objects.all()
    for service in services :
        # TODO: confirm that the service is valid for the given genomic region
        href = service.insert_genomic_region(sequence_name, start_pos, end_pos)
        hh.append(href)
        tt.append(service.name)

    aggregated_links = zip(hh, tt)
    context = {
        'linkout_type': 'genomic region',
        'label': '%s %s-%s'%(sequence_name, start_pos, end_pos),
        'aggregated_links': aggregated_links,
    }
    return context

