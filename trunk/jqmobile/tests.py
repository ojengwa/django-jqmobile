# http://docs.djangoproject.com/en/1.3/topics/testing/
from django.utils import unittest
from django.test.client import Client

class JqmobileTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_login(self):
        # Issue a GET request.
        response = self.client.get('/ma/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

#       # Check that the rendered context contains 5 customers.
#       self.assertEqual(len(response.context['customers']), 5)





# simulate normal request
# c = Client()
# response = c.post('/login/', {'username': 'john', 'password': 'smith'})
# response.status_code


# simulate ajax request
# c = Client()
# c.get('/customers/details/', {'name': 'fred', 'age': 7},
#      HTTP_X_REQUESTED_WITH='XMLHttpRequest')


# simulate post request

# c = Client()
# f = open('wishlist.doc')
# c.post('/customers/wishes/', {'name': 'fred', 'attachment': f})
# f.close()
