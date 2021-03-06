from django.shortcuts import render

from .models import InterMine

from intermine.webservice import Service
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
# TODO: complete the list of categories that are sequences and thus have a length field
sequence_categories = [
  'CDS', 'Chromosome', 'ConsensusRegion', 'Exon', 'Gene', 'GeneFlankingRegion',
  'GeneticMarker', 'IntergenicRegion', 'Intron', 'LinkageGroup', 'LinkageGroupRange',
  'MRNA', 'Protein', 'Supercontig', 'SyntenicRegion', 'TRNA'
]

# Construct value lists for (certain) template constraints
value_list_paths = [
  'Gene.chromosome.primaryIdentifier',
  'Gene.expressionValues.sample.description',
  'Gene.expressionValues.sample.primaryIdentifier',
  'Gene.flankingRegions.direction',
  'Gene.organism.name', 'Gene.organism.shortName',
  'GeneticMarker.chromosome.primaryIdentifier',
  'GWAS.results.phenotype.primaryIdentifier',
  'SyntenicRegion.chromosome.primaryIdentifier'
]
value_list_name_paths = [ 'Gene.organism.name', 'Gene.organism.shortName' ]

def getValueList(service, key) :
    if key not in value_list_paths :
        return None
    if key == 'GeneticMarker.chromosome.primaryIdentifier' :
        # workaround for LegumeMine (and others?),
        # original key does not return all of the desired chromosomes
        key = 'Gene.chromosome.primaryIdentifier'
    try :
        query = service.new_query(key)
        rset = set()
        for r in query.rows() :
            rset.add(r[0])
        rset.discard(None)
        rlist = sorted(list(rset), key = lambda s: s.lower())
        if key in value_list_name_paths :
            rlist = ['Any'] + rlist
        return rlist
    except :
        return None

# TODO: (currently low priority) Get sequence length from a remote FASTA file or URL
def getSequenceLength(url) :
    return 0

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
        base_url = im.url.rstrip('/')
        search_url = '%s/service/search?q=%s'%(base_url, keywords)
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

        try :
            im_total_hits = jj['totalHits']
        except :
            # PhytoMine does not have a totalHits field! Sum over those in its Categories.
            jjfcc = jj['facets']['Category']
            im_total_hits = 0
            for c in jjfcc :
                im_total_hits += jjfcc[c]
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
            base_url = im.url.rstrip('/')
            search_url = '%s/service/search?q=%s'%(base_url, keywords)
            if not (mine is None or mine == im.name) :
                continue
            if category is not None :
                search_url += '&facet_Category=%s'%(category)
            if organism is not None :
                search_url += '&facet_organism.shortName=%s'%(organism)
            search_url += '&start=%d'%(s)
            im_species = [ sp.get_short_name() for sp in im.species.all() ]

            rr = requests.get(search_url)
            jj = rr.json()
            new_results = jj['results']
            for r in new_results :
                result_id = r['id']
                r['url'] = '%s/report.do?id=%d&trail=|%d' % (base_url, result_id, result_id)
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
                # sequence information, if relevant
                if 'organism.shortName' in ff :
                    result_organism = ff['organism.shortName']
                elif 'organism.name' in ff :
                    organism_name = ff['organism.name'].split(' ')
                    result_organism = '%s. %s'%(organism_name[0][0], organism_name[1])
                # TODO: add length field for sequences
                if r['type'] in sequence_categories and (len(im_species) == 0 or (result_organism is not None and result_organism in im_species)) :
                    r['fasta_url'] = '%s/sequenceExporter.do?object=%d' % (base_url, result_id)
                    # r['fields']['length'] = getSequenceLength(r['fasta_url'])
                    r['blast_url'] = '%s/sequenceBlaster.do?object=%d' % (base_url, result_id)
            im_results[im.name] += new_results
            im_start[im.name] += len(new_results)
            if im_start[im.name] >= facets['Mine'][im.name] :
                im_start[im.name] = -1 # this mine's results are used up for paging purposes
            pth_results += new_results
            # (next mine)

        # Now we have enough results from each mine to consider for the pth page.
        # Sort results by relevance and return up to RESULTS_PER_PAGE of them
        pth_results = sorted(pth_results, key = lambda r: r['relevance'], reverse = True) # reverse = from_top
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

def templates(request) :
    # Determine available InterMines and associated templates
    selected_mines = request.GET.get('mines')
    if selected_mines is not None :
        selected_mines = selected_mines.split('+')
    existing_mines = []
    existing_templates = {}
    intermines = InterMine.objects.all()
    for im in intermines :
        existing_mines.append(im.name)
        if not (selected_mines is None or im.name in selected_mines) :
            continue
        base_url = im.url.rstrip('/')
        try :
            service = Service(base_url)
        except :
            # service is inaccessible, or some other error
            continue
        for t_name in service.templates :
            t = service.get_template(t_name)
            if t_name in existing_templates :
                existing_templates[t_name]['mines'].append(im.name)
            else :
                existing_templates[t_name] = {
                    'name': t.name,
                    'title': t.title,
                    'description': t.description,
                    'mines': [ im.name ]
                }
    # Sort existing_templates properly, and convert it to a list
    for t_name in existing_templates :
        existing_templates[t_name]['mines'] = sorted(existing_templates[t_name]['mines'], key = lambda m: m.lower())
    existing_templates = list(existing_templates.values())
    existing_templates = sorted(existing_templates, key = lambda t: t['title'].lower())

    context = {
        'existing_mines': existing_mines,
        'existing_templates': existing_templates,
        'user_mines': selected_mines,
    }
    return render(request, 'intermine_mgr/templates.html', context)

# Sort results (r) by a given sort tag (s)
def safeSort(r, s) :
    try :
        rs = r[s]
        return rs.lower()
    except :
        # move to last
        return chr(255)

def pathIsGeneRelated(path) :
    # also Gene.flankingRegions.direction (for SoyMine)?
    return path in [ 'Gene', 'Gene.primaryIdentifier', 'Gene.description' ]

def template_constraints(request) :
    mines_dict = {}
    intermines = InterMine.objects.all()
    for im in intermines :
        mines_dict[im.name] = im

    q = request.GET.get('q')
    qq = q.split('__')
    q_template = qq[0]
    q_mine_name = qq[1]
    q_mine = mines_dict[q_mine_name]
    base_url = q_mine.url.rstrip('/')
    # Note that q_service must exist if this template exists, so there is no need for a try/except here
    q_service = Service(base_url)
    selected_template = q_service.get_template(q_template)
    nc = len(selected_template.constraints) # number of constraints in selected_template

    constraints = []
    kw_constraints = {}
    gene_lists = q_service.get_all_list_names()
    gene_lists = [ l for l in gene_lists if q_service.get_list(l).list_type == 'Gene' ]
    base_filters_str = '?q=%s'%(q)
    use_default_constraints = False
    for i in range(nc) :
        stc_i = selected_template.constraints[i]
        stc_i_dict = stc_i.to_dict()
        is_gene_related = pathIsGeneRelated(stc_i.path)
        ch = chr(ord('A') + i)
        # constraints - return to template
        constraint = { 'code': ch, 'path': stc_i.path, 'edit': stc_i.editable, 'gene_related': is_gene_related }
        operator = request.GET.get('op' + ch)
        value = request.GET.get('value' + ch)
        value2 = request.GET.get('value2' + ch)
        value_list = getValueList(q_service, stc_i.path)
        if value_list is not None :
            constraint['value_list'] = value_list
        # organism_list is for the value2 (extraValue, extra_value) field in a ternary constraint
        organism_list = getValueList(q_service, 'Gene.organism.shortName')
        gene_operator = request.GET.get('gene_op' + ch)
        gene_value = request.GET.get('gene_value' + ch)
        if gene_operator is not None :
            # gene list-based constraint
            # (set operator and value for use in kw_constraints below)
            constraint['gene_op'] = operator = gene_operator
            constraint['gene_value'] = value = gene_value
            constraint['op'] = stc_i.op
            constraint['value'] = stc_i.value
            if 'extraValue' in stc_i_dict :
                constraint['value2'] = stc_i_dict['extraValue']
            constraints.append(constraint)
            if stc_i.editable :
                base_filters_str += '&op%s=%s&value%s=%s&gene_op%s=%s&gene_value%s=%s'%(ch, stc_i.op, ch, stc_i.value, ch, gene_operator, ch, gene_value)
        elif operator is not None :
            # regular (binary) constraint
            constraint['op'] = operator
            constraint['value'] = value
            if value2 is not None :
                # ternary constraint
                constraint['value2'] = value2
                if organism_list is not None :
                    constraint['value_list'] = organism_list
            constraints.append(constraint)
            if stc_i.editable :
                base_filters_str += '&op%s=%s&value%s=%s'%(ch, operator, ch, value)
                if value2 is not None :
                    base_filters_str += '&value2%s=%s'%(ch, value2)
        else :
            # user submitted no constraints (yet), so use default values from selected template
            use_default_constraints = True
            try :
                constraint['op'] = stc_i.op
                constraint['value'] = stc_i.value
                if 'extraValue' in stc_i_dict :
                    constraint['value2'] = stc_i_dict['extraValue']
                    if organism_list is not None :
                        constraint['value_list'] = organism_list
                constraints.append(constraint)
            except :
                # ignore if any fields are missing
                pass
            continue # so as not to submit default values to template query

        if stc_i.editable :
            # kw_constraints - submit to template query
            kw_constraints[ch] = { 'op': operator, 'value': value }
            if value2 not in [ None, 'Any' ] :
                kw_constraints[ch]['extra_value'] = value2

    if use_default_constraints :
        context = {
            'user_q': q,
            'user_mine': q_mine_name,
            'user_template': selected_template,
            'user_constraints': constraints,
            'gene_lists': gene_lists,
        }
        return render(request, 'intermine_mgr/template_constraints.html', context)

    # Paging
    page = request.GET.get('page')
    if page is None :
        page = 1
    else :
        page = int(page)
    results_per_page = request.GET.get('rows')
    # Note that start indices are 0-based in the view, 1-based in the template
    if results_per_page is None :
        start = 0
    else :
        results_per_page = int(results_per_page)
        start = (page - 1)*results_per_page

    # Extract facet filters (only mines, for now)
    facet_filters = {}
    facet_filters_str = ''
    mine = request.GET.get('Mine')
    if mine :
        facet_filters['Mine'] = mine
        facet_filters_str += '&Mine=' + mine

    facets = { 'Mine': {} }
    total_hits = 0
    results = []
    for im in intermines :
        if not (mine is None or mine == im.name) :
            continue
        base_url = im.url.rstrip('/')
        try :
            service = Service(base_url)
        except :
            # service is inaccessible, or some other error
            continue
        try :
            template = service.get_template(q_template)
            # Execute the (possibly modified) query
            rr = template.rows(**kw_constraints)
            for row in rr :
                rd = row.to_d()
                rd.update({ 'mine': im.name })
                results.append(rd)
            im_total_hits = len(rr)
            total_hits += im_total_hits
            # Aggregating facets is more complicated:
            facets['Mine'][im.name] = im_total_hits
        except :
            # For example, if the constraints do not apply to the template for this mine
            continue
    # This yields the total hits and facet information.
    # Remove any mines with no hits.
    mm = list(facets['Mine'].keys())
    for m in mm :
        if facets['Mine'][m] == 0 :
            del facets['Mine'][m]

    sort_tag = selected_template.get_sort_order().sort_orders[0].path # TODO: sort by multiple columns?
    results = sorted(results, key = lambda result: safeSort(result, sort_tag))
    if results_per_page is None :
        end = total_hits
        last_page = 1
    else :
        end = min(start + results_per_page, total_hits)
        results = results[start:end]
        last_page = (total_hits - 1) // results_per_page + 1
        base_filters_str += '&rows=%d'%(results_per_page)
    context = {
        'user_q': q,
        'user_mine': q_mine_name,
        'user_template': selected_template,
        'user_constraints': constraints,
        'gene_lists': gene_lists,
        'base_filters_str': base_filters_str,
        'facet_filters': facet_filters,
        'facet_filters_str': facet_filters_str,
        'page': page,
        'results_per_page': results_per_page,
        'last_page': last_page,
        'start_row': start + 1,
        'end_row': end,
        'num_rows': total_hits,
        'results': results,
        'facets': facets,
    }

    return render(request, 'intermine_mgr/template_constraints.html', context)

