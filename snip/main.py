import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
    	self.response.headers["Content-Type"] = ""
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

application = webapp2.WSGIApplication([
    ('/app/hello', MainPage),
], debug=True)
