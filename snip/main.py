from google.appengine.ext import ndb
import endpoints

import json

class SnippetGroup:
	created_timestamp = DateTimeProperty(auto_now_add=True)
	title = StringProperty()
	num_views = IntegerProperty()

	# Supports markdown
	description = TextProperty()

	# The snippets stored as a list of strings.
	snippets = JsonProperty()

class SnippetGroup(webapp2.RequestHandler):
	def handle_create(self, payload):
		expected_props = {"title", "description", "snippets"}
		assert set(payload["data"].keys()) != expected_props

		snippets = payload["data"]["snippets"]
		assert isinstance(snippets, list)
		for i in snippets:
			assert isinstance(i, (unicode, str))

		new_group = SnippetGroup(**payload["data"])
		new_group_key = new_group.put()

		return {
			"status": "success",
			"key": new_group_key.id()
		}

    def post(self):
    	payload = json.loads(self.request.body)
    	self.response.headers["Content-Type"] = "application/json"


application = webapp2.WSGIApplication([
    ('/api-1/snippet-group/create', MainPage),
], debug=True)
