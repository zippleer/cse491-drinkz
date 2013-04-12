import urlparse, simplejson
from jinja2 import Environment  
from urllib2 import urlopen
from json import load


begining = """ \
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
        <title> %s </title>
    </head>
	<body>
		<div class="container">
            <h1 class="head">%s</h1>
            <article>""" 
end = """ 	</article>
		</div>
	</body>
</html>"""

class AppClass(object):
    def __call__(self, environ, start_response):
        status = '200 OK'

        path = environ['PATH_INFO']
        data = ""
        title = "Application"
        content = " "

        if path == '/':
            content_type = 'text/html'
            title = "WSGI AppClass"
            content = """<p>Application/Framework</p><br><a href='/form'> Input Form Data </a><br><a href='/pic'>Retrieve Picture</a><br>"""

            data = begining % (title,title) + content + end 
        elif path == '/form':
            content_type = 'text/html'
            title = "form"
            content = """
            <form action='recv'>
            Give me some input ffs!: <input type='text' size='30' name='in'> <input type='submit'></form>"""

            data = begining % (title,title) + content + end 
        elif path == '/recv':
            content_type = 'text/html'
            title = 'form'
            content= """User Input=%s"""
            response = environ['QUERY_STRING']
            results = urlparse.parse_qs(response)

            resp = results['in']
            
            data = begining % (title,title) + content%resp[0] + end 
        elif path == '/pic':
            content_type = 'image/gif'
            data = open('Spartan-hemlet-Black-150-pxls.gif','rb').read()
            
        else:
            content_type = 'text/plain'
            data = 'Path Request %s' % environ['PATH_INFO']
        headers = [('Content-type', content_type)]
        start_response('200 OK', headers)

        return [data]
