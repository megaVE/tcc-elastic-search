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

@app.get('/')
def index():
    """Renders the Home Page"""
    return render_template('index.html')


@app.post('/')
def handle_search():
    """Handles the search from the Home Page"""
    query = request.form.get('query', '')
    from_ = request.form.get('from_', type=int, default=0)
    results = es.search(
        index=index_name,
        query={
            #  SINGLE FIELD MATCHING QUERY
            # 'match': {
            #     'name': {
            #         'query': query
            #     }
            # }
            
            'multi_match': {
                'query': query,
                'fields': searchable_fields
            },
        },
        size=max_results_per_page,
        from_=from_
    )
    return render_template(
        'index.html',
        query=query, # the query text entered by the user in the form
        results=results['hits']['hits'], # a list of search results
        from_=from_, #the zero-based index of the first result
        total=results['hits']['total']['value'] # the total number of results
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
 