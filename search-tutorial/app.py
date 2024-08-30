import re
from flask import Flask, render_template, request
from search import Search

from dotenv import load_dotenv
import os

app = Flask(__name__)
es = Search()

load_dotenv()

index_name = os.environ['INDEX']

searchable_fields = ['name', 'summary', 'content']
data_file_path = "data.json"

max_results_per_page = 5

def extract_filters(query):
    filters = []
    
    filter_regex = r'category:([^\s]+)\s*'
    m = re.search(filter_regex, query)
    if m:
        filters.append({
            'term': {
                'category.keyword': {
                    'value': m.group(1)
                }
            }
        })
        query = re.sub(filter_regex, '', query).strip()        
    
    filter_regex = r'year:([^\s]+)\s*'
    m = re.search(filter_regex, query)
    if m:
        filters.append({
            'range': {
                'updated_at': {
                    'gte': f'{m.group(1)}||/y',
                    'lte': f'{m.group(1)}||/y'
                }
            }
        })
        query = re.sub(filter_regex, '', query).strip()
    
    return {'filter': filters}, query

@app.get('/')
def index():
    """Renders the Home Page"""
    return render_template('index.html')


@app.post('/')
def handle_search():
    """Handles the search from the Home Page"""
    query = request.form.get('query', '')
    filters, parsed_query = extract_filters(query=query)
    from_ = request.form.get('from_', type=int, default=0)
    
    if parsed_query:
        search_query = {
            'must': [{
                'multi_match': {
                    'query': parsed_query,
                    'fields': ['name', 'summary', 'content'],
                }
            }]
        }
    else:
        search_query = {
            'must': {
                'match_all': {}
            }
        }
    
    results = es.search(
        index=index_name,
        query={
            'bool': {
                **search_query,
                **filters
            }
            
            # 1-SINGLE FIELD MATCHING QUERY
            # 'match': {
            #     'name': {
            #         'query': query
            #     }
            # }
            
            # 2-MULTI FIELD MATCHING QUERY
            # 'multi_match': {
            #     'query': query,
            #     'fields': searchable_fields
            # }

            # 3-BOOLEAN QUERY            
            # 'bool': {
            #     'must': [{
            #         'multi_match': {
            #             'query': parsed_query,
            #             'fields': ['name', 'summary', 'content'],
            #         }
            #     }],
            #     **filters
            #     # 'filter': [{
            #     #     'term': {
            #     #         'category.keyword': {
            #     #             'value': "category to filter"
            #     #         }
            #     #     }
            #     # }]
            # } 
        },
        aggs={
            'category-agg': {
                'terms': {
                    'field': 'category.keyword',
                }
            },
            'year-agg': {
                'date_histogram': {
                    'field': 'updated_at',
                    'calendar_interval': 'year',
                    'format': 'yyyy'
                }
            }
        },
        size=max_results_per_page,
        from_=from_
    )
    
    aggs = {
        'Category': {
            bucket['key']: bucket['doc_count']
            for bucket in results['aggregations']['category-agg']['buckets']
        }
    }
    
    return render_template(
        'index.html',
        query=query, # the query text entered by the user in the form
        results=results['hits']['hits'], # a list of search results
        from_=from_, #the zero-based index of the first result
        total=results['hits']['total']['value'], # the total number of results
        aggs=aggs
    )


@app.get('/document/<id>')
def get_document(id):
    """Renders a given document"""
    try:
        document = es.retrieve_document(index=index_name, id=id)
        title = document['_source']['name']
        paragraphs = document['_source']['content'].split('\n')
        return render_template('document.html', title=title, paragraphs=paragraphs)
    except:
        return render_template('document.html', title="Document not found")

@app.cli.command()
def reindex():
    """Regenerate the Elasticsearch index."""
    response = es.reindex(file_path=data_file_path, index=index_name)
    print(f'Index "{index_name}" with {len(response["items"])} documents created '
        f'in {response["took"]} miliseconds.')
 