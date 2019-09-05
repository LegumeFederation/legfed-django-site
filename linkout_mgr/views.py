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
        jj = service.get_linkouts(gene)
        for j in jj :
            if 'error' in j :
                continue
            href = j['href']
            # TODO: confirm whether to prepend 'http:'
            if (not href.startswith('http')) :
                href = 'http:' + href
            hh.append(href)
            tt.append(j['text'])

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
        jj = service.get_linkouts(sequence_name, start_pos, end_pos)
        for j in jj :
            if 'error' in j :
                continue
            href = j['href']
            # TODO: confirm whether to prepend 'http:'
            if (not href.startswith('http')) :
                href = 'http:' + href
            hh.append(href)
            tt.append(j['text'])

    aggregated_links = zip(hh, tt)
    context = {
        'linkout_type': 'genomic region',
        'label': '%s %s-%s'%(sequence_name, start_pos, end_pos),
        'aggregated_links': aggregated_links,
    }
    return context

def test(request) :
    linkout_type = display_linkout_type = ''
    if request.method == 'GET' :
        linkout_type = request.GET.get('linkout_type')

    nt = 0
    failed_tests = []
    services = []
    if linkout_type == 'gene' :
        display_linkout_type = 'Gene'
        services = GeneLinkout.objects.all()
    elif linkout_type == 'genomic_region' :
        display_linkout_type = 'Genomic Region'
        services = GenomicRegionLinkout.objects.all()

    for service in services :
        jj = service.get_example_linkouts()
        # The following assumes that each related linkout has the same issues,
        # so we need only display the first one (j0)
        j0 = jj[0]
        if 'error' in j0 :
            failed_tests += [ j0 ] #[(j0['text'], j0['error'], j0['href'])]
        nt += 1
    np = nt - len(failed_tests)
    pct = 0
    if nt > 0 :
        pct = np*100.0/nt

    context = {
        'linkout_type': display_linkout_type,
        'num_tests_passed': np,
        'num_tests_total': nt,
        'pct_tests_passed': '%2.1f'%(pct),
        'failed_tests_list': failed_tests,
    }
    return render(request, 'linkout_mgr/test.html', context)

