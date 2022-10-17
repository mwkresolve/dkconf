
from .models import User
from .functionsdb import create_user_game, update_reputation
import names
import random
import unittest

class CaseCreateUser(unittest.TestCase):
    def testBasic(self):
    	for c in range(10):
    		name = f'{names.get_last_name()}_{names.get_first_name()}'
    		print(name)
    		self.user_1 = User.objects.create_user(f'{name}', f'{name}@chase.com', 'chevyspgererassword')
    		create_user_game(self.user_1)
    		update_reputation(self.user_1, random.randint(100, 10000))


