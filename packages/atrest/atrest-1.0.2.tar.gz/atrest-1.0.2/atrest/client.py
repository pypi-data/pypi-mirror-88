import requests
from atrest.api import API


class Client:
    def __init__(self, at_base_url, at_integration_code, at_username, at_secret):
        self.api = API(at_base_url, at_integration_code, at_username, at_secret)

    def query_tickets(self, ticket_id) -> requests.Response:
        """
        Query for a ticket by ticket id.
        Returns either the ticket information in json, or raises an exception.
        """
        return self.api.query_tickets(ticket_id)

    def create_ticket(
        self, title, description, status, priority, company_id, queue_id
    ) -> int:
        """
        Create a ticket.
        Returns either the ticket ID of the created ticket, or raises an exception.
        """
        return self.api.create_ticket(
            title, description, status, priority, company_id, queue_id
        )

    def add_ticket_attachment(
        self, ticket_id, attachment_heading, file_name, b64_encoded_attachment
    ) -> int:
        """
        Create a ticket.
        Returns either the ticket ID of the created ticket, or raises an exception.

        Attachment needs to be base64 encoded:
        # import base64
        # data = open("sample.txt", "r").read()
        # encoded = base64.b64encode(data.encode('utf-8'))
        # add_ticket_attachment(self, ticket_id, encoded)
        """
        return self.api.add_ticket_attachment(
            ticket_id, attachment_heading, file_name, b64_encoded_attachment
        )

    def create_ticket_with_attachment(
        self,
        title,
        description,
        status,
        priority,
        company_id,
        queue_id,
        attachment_heading,
        file_name,
        b64_encoded_attachment,
    ):
        """
        Create a ticket and updates it with an attachment.
        Returns either the ticket ID of the created ticket, or raises an exception.

        Attachment needs to be base64 encoded:
        # import base64
        # data = open("sample.txt", "r").read()
        # encoded = base64.b64encode(data.encode('utf-8'))
        # add_ticket_attachment(self, ticket_id, encoded)
        """

        ticket_id = self.api.create_ticket(
            title, description, status, priority, company_id, queue_id
        )

        self.api.add_ticket_attachment(
            ticket_id, attachment_heading, file_name, b64_encoded_attachment
        )

        return ticket_id