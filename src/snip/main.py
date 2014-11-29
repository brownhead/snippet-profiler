from google.appengine.ext import ndb
import webapp2

import struct
import json
import base64
import datetime

def encode_id(numeric_id):
    return base64.urlsafe_b64encode(struct.pack("!Q", numeric_id)).rstrip("=")

def decode_id(encoded_id):
    padding = "=" * (len(encoded_id) % 3)
    return struct.unpack("!Q", base64.urlsafe_b64decode(encoded_id + padding))[0]

def json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()

class SnippetGroup(ndb.Model):
    SERIALIZED_WHITELIST = ["created_timestamp", "title", "num_views", "description", "snippets"]

    created_timestamp = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    num_views = ndb.IntegerProperty()

    # Supports markdown
    description = ndb.TextProperty()

    snippets = ndb.TextProperty(repeated=True)

class SnippetGroupEndpoints(webapp2.RequestHandler):
    def handle_create(self, payload):
        expected_attrs = {"title", "description", "snippets"}
        assert set(payload["data"].keys()) == expected_attrs

        snippets = payload["data"]["snippets"]
        assert isinstance(snippets, list)
        for i in snippets:
            assert isinstance(i, (unicode, str))

        new_key = SnippetGroup(**payload["data"]).put()

        # We encode the key by transforming it into an 8-byte, network-byte-order binary
        # representation and then converting that into a base64 string without padding.
        encoded_key = base64.urlsafe_b64encode(struct.pack("!Q", new_key.id())).rstrip("=")

        return {"status": "success", "key": encode_id(new_key.id())}

    def handle_get(self, key_id):
        decoded_id = decode_id(key_id)
        group = SnippetGroup.get_by_id(decoded_id)

        return {
            "status": "success",
            "data": {k: getattr(group, k) for k in SnippetGroup.SERIALIZED_WHITELIST},
        }

    def get(self, key_id):
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(json.dumps(self.handle_get(key_id), default=json_default))

    def post(self):
        payload = json.loads(self.request.body)
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(json.dumps(self.handle_create(payload)))


application = webapp2.WSGIApplication([
    ('/api-1/snippet-group/create', SnippetGroupEndpoints),
    ('/api-1/snippet-group/([^/]+)', SnippetGroupEndpoints),
], debug=True)
