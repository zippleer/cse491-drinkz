import sys
import simplejson
import urllib2

def call_remote(base, method, params, id):
    # determine the URL to call
    url = base + 'rpc'

    # encode things in a dict that is then converted into JSON
    d = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(d)

    # specify appropriate content-type
    headers = { 'Content-Type' : 'application/json' }

    # call remote server
    req = urllib2.Request(url, encoded, headers)

    print "CALLED REMOTE"

    # get response
    response_stream = urllib2.urlopen(req)
    json_response = response_stream.read()

    print "GOT RESPONSE"
    print json_response
    print "++++++"

    # decode response
    response = simplejson.loads(json_response)

    print "DECODED RESPONSE"

    # return result
    return response['result']

if __name__ == '__main__':
    server_base = sys.argv[1]

    print 'convert:', call_remote(server_base, method='convert_units_to_ml', params=['1 oz'], id=1)
