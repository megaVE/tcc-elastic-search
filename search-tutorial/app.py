import re
from flask import Flask, render_template, request
from search import Search

app = Flask(__name__)
es = Search()

@app.get('/')
def index():
    """Renders the Home Page"""
    return render_template('index.html')


@app.post('/')
def handle_search():
    """Handles the search from the Home Page"""
    query = request.form.get('query', '')
    return render_template(
        'index.html', query=query, results=[], from_=0, total=0)


@app.get('/document/<id>')
def get_document(id):
    return 'Document not found'

@app.cli.command()
def reindex():
    """Regenerate the Elasticsearch index."""
    response = es.reindex(file_path='data.json', index='my_documents')
    print(f'Index with {len(response["items"])} documents created '
        f'in {response["took"]} miliseconds.')
 