import webapp2
import urllib
import re

import audio_fetch

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import channel

# portal, in other words, index.html
class MainPage(webapp2.RequestHandler):
#	upon a get request
	def get(self):
		self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

		upload_url = blobstore.create_upload_url('/upload')
#		naive approach at the moment TODO
		main = open("web/test.html", "r")
		for l in main:
			if re.search("<!--INSERT-SUBMIT-->", l):
				self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
				self.response.out.write("""Upload File: <input type="file" name="file"> <input type="submit" name="submit" value="Submit"> </form>""")
			else:
				self.response.write(l)
		main.close()
	

# womp - just taking space
class DevPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('dev page')

class AboutPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('who we are, what we did')

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		blobkey = blob_info.key()
#		play what you uploaded
		self.send_blob(blob_info)
#		now send the bytestream
		blob_reader = blobstore.BlobReader(blobkey)
		value = blob_reader.read()
		data = audio_fetch.UploadFile(value)		

application = webapp2.WSGIApplication([
#	define the page tree here
	('/', MainPage),
	('/dev', DevPage),
	('/about', AboutPage),
	('/upload', UploadHandler),
	('/serve/([^/]+)?', ServeHandler),
], debug=True)
