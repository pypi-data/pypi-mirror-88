import os, sys
from dotenv import load_dotenv
from .api import API

sys.tracebacklimit = 0

class Client:

    def __init__(self):
        self.api = API()

    def get_base_url(self):
        return self.api.get_base_url()

    def set_base_url(self, base_url):
        self.api.base_url = base_url

    def get_headers(self):
        return self.api.get_headers()

    def set_headers(self, api_integration_code=None, username=None, secret=None):
        self.api.set_headers(api_integration_code, username, secret)

    def query_tickets(self):
        return self.api.query_tickets()

    def create_ticket(self, title, description, status, priority, company_id, queue_id):
        return self.api.create_ticket(title, description, status, priority, company_id, queue_id)


# at = Client()

# print(at.get_headers())
# at.set_headers(username="otherapiuser@strivehealth.com")
# print(at.get_headers())

# print()

# print(at.get_base_url())
# at.set_base_url("http://fake!")
# print(at.get_base_url())

# print(at.query_tickets())
# print(at.create_ticket("Bitdefender Alert", "We detected a blocked application."))