import webapp2

class MainPage(webapp2.RequestHandler):
#	upon a get request
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('indev')
	
application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
