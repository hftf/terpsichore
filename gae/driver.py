import webapp2

class MainPage(webapp2.RequestHandler):
#	upon a get request
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('main page')

class DevPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('dev page')

application = webapp2.WSGIApplication([
#	define the application tree here
	('/', MainPage),
	('/dev', DevPage),
], debug=True)
