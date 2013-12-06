from wikitools import wiki, api

"""
An extremely basic wrapper for the wikitools api.
"""
site = wiki.Wiki() # This defaults to en.wikipedia.org
query_params['action'] = 'query'
request = api.APIRequest(site, query_params)
result = request.query()
