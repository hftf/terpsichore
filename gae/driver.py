import webapp2

class MainPage(webapp2.RequestHandler):
#	upon a get request
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
#		naive approach at the moment TODO
		main = open("web/test.html", "r")
		text = ""
		for l in main:
			text += l
		main.close()
		self.response.write(text)

class DevPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('dev page')

application = webapp2.WSGIApplication([
#	define the application tree here
	('/', MainPage),
	('/dev', DevPage),
], debug=True)
