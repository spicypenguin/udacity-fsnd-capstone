import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import db


class FatpenguinCastingTestCase(unittest.TestCase):
    def setUp(self):
        APP.config['SQLALCHEMY_DATABASE_URI'] = f"postgres://castingagency:password12345@localhost:5432/castingagency-test"
        self.app = APP
        self.client = self.app.test_client

        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')

        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actors'], list)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
