from django.shortcuts import render

from .models import InterMine

import requests

from legfedsite.private_settings import INTERMINE_CONTACT_EMAIL

# TODO: Fill in the commented ones. Is there a complete list?
category2identifiers = {
  #'Annotatable': [],
  'Author': [ 'name' ],
  #'Bio-Entity': [],
  'CDS': [ 'primaryIdentifier' ],
  #'COAnnotation': [],
  'COTerm': [ 'identifier', 'name' ],
  'Chromosome': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  #'Comment': [],
  'Component': [],
  'ConsensusRegion': [ 'primaryIdentifier' ],
  #'CrossReference': [],
  'DataSet': [ 'name' ],
  'DataSource': [ 'name' ],
  'ECNumber': [],
  'Exon': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  #'Experiment': [],
  'ExpressionSample': [ 'primaryIdentifier' ],
  'ExpressionSource': [ 'primaryIdentifier' ],
  'ExpressionValue': [],
  #'GOAnnotation': [],
  'GOEvidence': [],
  'GOEvidenceCode': [],
  'GOTerm': [ 'identifier', 'name' ],
  'GWAS': [ 'primaryIdentifier' ],
  'GWASResult': [],
  'Gene': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'GeneFamily': [ 'primaryIdentifier' ],
  'GeneFlankingRegion': [ 'primaryIdentifier' ],
  'Generif': [],
  'GeneticMap': [ 'primaryIdentifier' ],
  'GeneticMarker': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'GenotypeValue': [],
  'GenotypingStudy': [],
  'Homologue': [],
  'IntergenicRegion': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'Intron': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'LinkageGroup': [ 'primaryIdentifier' ],
  'LinkageGroupPosition': [],
  'LinkageGroupRange': [],
  #'Location': [],
  'MRNA': [ 'primaryIdentifier' ],
  'MappingPopulation': [],
  #'ncRNA': [],
  'Ontology': [ 'name' ],
  #'OntologyAnnotation': [],
  #'OntologyRelation': [],
  'OntologyTerm': [ 'identifier', 'name' ],
  'OntologyTermSynonym': [],
  'Organism': [ 'taxonId' ],
  'OrthologueEvidence': [],
  'OrthologueEvidenceCode': [],
  #'POAnnotation': [],
  'POTerm': [ 'identifier', 'name' ],
  'Pathway': [ 'name' ],
  'Phenotype': [ 'primaryIdentifier' ],
  'PhenotypeValue': [],
  'Protein': [ 'primaryIdentifier' ],
  'ProteinDomain': [ 'primaryIdentifier' ],
  'ProteinDomainRegion': [],
  'ProteinHmmMatch': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'ProteinMatch': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'Publication': [ 'pubMedId' ],
  'QTL': [ 'primaryIdentifier' ],
  'RnaseqExperiment': [],
  'RnaseqExpression': [],
  'SOTerm': [ 'identifier', 'name' ],
  #'Sequence': [],
  #'SequenceFeature': [],
  'Strain': [],
  'Supercontig': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  #'Synonym': [],
  'SyntenicRegion': [ 'primaryIdentifier' ],
  'SyntenyBlock': [ 'primaryIdentifier' ],
  #'TOAnnotation': [],
  'TOTerm': [ 'identifier', 'name' ],
  'TRNA': [ 'primaryIdentifier' ],
  'TentativeConsensus': [ 'primaryIdentifier' ],
  #'Transcript': [],
  'TransposableElementGene': [ 'primaryIdentifier', 'secondaryIdentifier' ],
  'UniProtFeature': [],
}

# Sort results by relevance
def byRelevance(result) :
    return result['relevance']

# Create your views here.
def index(request) :
    keywords = request.GET.get('keywords')
    if keywords is None :
        context = { 'keywords': '', }
        return render(request, 'intermine_mgr/index.html', context)

    start = request.GET.get('start')
    if start is None :
        start = 1
    else :
        start = int(start)
    # Note that start indices are 0-based in the view, 1-based in the template
    start -= 1

    # Extract facet filters
    facet_filters = {}
    facet_filters_str = ''
    mine = request.GET.get('Mine')
    if mine :
        facet_filters['Mine'] = mine
        facet_filters_str += '&Mine=' + mine
    category = request.GET.get('Category')
    if category :
        facet_filters['Category'] = category
        facet_filters_str += '&Category=' + category
    organism = request.GET.get('organism.shortName')
    if organism :
        facet_filters['organism.shortName'] = organism
        facet_filters_str += '&organism.shortName=' + organism

    # Aggregate the results
    RESULTS_PER_PAGE = 100
    # First pass: get the facet information and total hits
    intermines = InterMine.objects.all()
    facets = { 'Mine': {} }
    total_hits = 0
    for im in intermines :
        # This assumes that the search URL is always of the form <im.url>/service/search?q=<keywords>
        # and that for result details is always of the form <im.url>/report.do?<...>
        # TODO: generalize for other expected formats.
        search_url = '%s/service/search?q=%s'%(im.url, keywords)
        if not (mine is None or mine == im.name) :
            continue
        if category is not None :
            search_url += '&facet_Category=%s'%(category)
        if organism is not None :
            search_url += '&facet_organism.shortName=%s'%(organism)

        # TODO: catch RequestExceptions including traceback if possible
        #try :
            #rr = requests.get('http://www.google.com/nothere')
            #rr.raise_for_status()
        rr = requests.get(search_url)
        jj = rr.json()
        status_code = jj['statusCode']
        #except requests.exceptions.RequestException as e :
        if status_code != 200 :
            context = {
                'error_message': jj['error'],
                'error_recipient': INTERMINE_CONTACT_EMAIL,
                'error_status_code': status_code,
                'error_subject': 'Error found on %s website'%(im.name),
            }
            return render(request, 'intermine_mgr/index.html', context)

        im_total_hits = jj['totalHits']
        total_hits += im_total_hits
        # Aggregating facets is more complicated:
        facets['Mine'][im.name] = im_total_hits
        im_facets = jj['facets']
        for k1 in im_facets :
            if k1 not in facets :
                facets[k1] = {}
            for k2 in im_facets[k1] :
                if k2 not in facets[k1] :
                    facets[k1][k2] = 0
                facets[k1][k2] += im_facets[k1][k2]
    # This yields the total hits and facet information.
    # Remove any mines with no hits.
    mm = list(facets['Mine'].keys())
    for m in mm :
        if facets['Mine'][m] == 0 :
            del facets['Mine'][m]
    if total_hits == 0 :
        context = {
            'keywords': keywords,
            'num_rows': total_hits,
        }
        return render(request, 'intermine_mgr/index.html', context)
    start_last = (total_hits - 1) // RESULTS_PER_PAGE * RESULTS_PER_PAGE

    # TODO: If start is closer to the top, work down. If closer to the bottom, work up.
    # from_top = (start <= total_hits - start)

    # Second pass(es): Correctly handle results paging across multiple mines
    num_pages = start // 100 + 1
    im_start = {}
    im_results = {}
    for im in intermines :
        im_start[im.name] = 0
        im_results[im.name] = []
#    results = []
    for p in range(num_pages) :
        pth_results = []
        pth_count = {}
        for im in intermines :
            if im.name not in facets['Mine'] :
                continue
            pth_results += im_results[im.name]
            pth_count[im.name] = 0
            s = im_start[im.name]
            if s < 0 or len(im_results[im.name]) >= RESULTS_PER_PAGE :
                continue
            search_url = '%s/service/search?q=%s'%(im.url, keywords)
            if not (mine is None or mine == im.name) :
                continue
            if category is not None :
                search_url += '&facet_Category=%s'%(category)
            if organism is not None :
                search_url += '&facet_organism.shortName=%s'%(organism)
            search_url += '&start=%d'%(s)

            rr = requests.get(search_url)
            jj = rr.json()
            new_results = jj['results']
            for r in new_results :
                result_id = r['id']
                r['url'] = '%s/report.do?id=%d&trail=|%d' % (im.url, result_id, result_id)
                ff = r['fields']
                r['identifiers'] = ii = category2identifiers[r['type']]
                ni = len(ii)
                for n in range(ni) :
                    try :
                        r['label%d'%(n + 1)] = ff[ii[n]]
                    except :
                        r['label%d'%(n + 1)] = '-'
                if ni == 0 :
                    r['label1'] = r['type']
                r['mine'] = im.name
            im_results[im.name] += new_results
            im_start[im.name] += len(new_results)
            if im_start[im.name] >= facets['Mine'][im.name] :
                im_start[im.name] = -1 # this mine's results are used up for paging purposes
            pth_results += new_results
            # (next mine)

        # Now we have enough results from each mine to consider for the pth page.
        # Sort results by relevance and return up to RESULTS_PER_PAGE of them
        pth_results = sorted(pth_results, key = byRelevance, reverse = True) # reverse = from_top
        num_results = min(len(pth_results), RESULTS_PER_PAGE)
        results = pth_results[:num_results]
        # Discard already-used results from this page
        for i in range(num_results) :
            r = pth_results[i]
            pth_count[r['mine']] += 1
        for im in intermines :
            if im.name not in facets['Mine'] :
                continue
            im_results[im.name] = im_results[im.name][pth_count[im.name]:]
        # (next page)

    context = {
        'keywords': keywords,
        'facet_filters': facet_filters,
        'facet_filters_str': facet_filters_str,
        'start_row': start + 1,
        'end_row': start + num_results,
        'num_rows': total_hits,
        'start_prev': max(start - RESULTS_PER_PAGE, 0) + 1,
        'start_next': min(start + RESULTS_PER_PAGE, start_last) + 1,
        'start_last': start_last + 1,
        'results': results,
        'facets': facets,
    }

    return render(request, 'intermine_mgr/index.html', context)

