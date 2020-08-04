import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import db

casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdCY1RHaFFic0lRX3BQaTFKTnVMVSJ9.eyJpc3MiOiJodHRwczovL2ZhdHBlbmd1aW4tY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMyNzM5MTYwNjA3Nzc2MDM3OTEiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2ZhdHBlbmd1aW4tY2FzdGluZy51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NTI2MDQxLCJleHAiOjE1OTY1MzMyNDEsImF6cCI6IktTYnhrbmYyTGp1MUF0NUxjVnNGdk4yNkp6Mk4xRjJQIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.jp0ivSaGt2f_Wx6lRtEGe7iUlMqUE3OJAVjdiUeZDWNANb3GQgZgD01d8SbqB2g-ccipsf7yzU-Rpw6crGnuWR-GGGOclFUdIfRyNrLm3-gtxwo_UhQNjoJ-FZbdGKbWVTMlyIbMWB7ELD8mhKC6KoaHFnKl08usWjgXtEcl0maEaKJ34JKHdpiEzpwagYu9jU2L041SFF4iPp5alxzZ5PfSN4SSIa_YG55mCleDksOoPGGHXnJxkT6j2do0PK4hEJpiFPZ2o_auUp7EecB6IYQUR5WaXcDKEhdjNjErhlPuWnWFdEc_r0H9DexQRi_XV9EtWmw2Ad8QCZ29S88pwA'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdCY1RHaFFic0lRX3BQaTFKTnVMVSJ9.eyJpc3MiOiJodHRwczovL2ZhdHBlbmd1aW4tY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyOGQwMTljMTNiMTMwMjI4Zjg1Y2Q1IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTY1MjI5OTksImV4cCI6MTU5NjUzMDE5OSwiYXpwIjoiS1NieGtuZjJManUxQXQ1TGNWc0Z2TjI2SnoyTjFGMlAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6cm9sZSIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6cm9sZSIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyJdfQ.IIB_F7Bkn80qs_RhS4aZNtyJnwXPIK2VftXWwClZoxrMYUwd-19lfvMwbSzadA4GLnMm1y4KqUbHGssQaMusj_h1s654gp3xTzuT4gkWboZfDn46FsoX0Wbq080Ujm9SvqKOgjLWy85YwVTQhH1tLdIsRB7bvnNU2rllRrN6jaUTspQdYEP1DKKUwEdrz9-am-W3diQ84fuzgOYrXDs43SUTMLFYLuOyvrcbfeHnP3kNAw2twavosv1IRmIbejr0ufA_6OhG5but9LKdmWKaIuMNa6_6XL69VRD2CdafR9SsRWUtNiIPZ3RRsLCsIkO9Bs1NhxnJVymD7OjWz0LJUg'
executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdCY1RHaFFic0lRX3BQaTFKTnVMVSJ9.eyJpc3MiOiJodHRwczovL2ZhdHBlbmd1aW4tY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyOGQwMzMyNTdiMDAwMDM4ZTQ2YWU1IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTY1MjQ4OTQsImV4cCI6MTU5NjUzMjA5NCwiYXpwIjoiS1NieGtuZjJManUxQXQ1TGNWc0Z2TjI2SnoyTjFGMlAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiY3JlYXRlOnJvbGUiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImRlbGV0ZTpyb2xlIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.NQYKmEz0t2aJFQpIaymGQTYQrxeEDMq5SlZV1v1592SSHN3aV-jRaXySbW4UzVlLr4zDIqMWzxne7_jrhcqJWXnvP2XBjhtlXHOIgR28ryRvAQMtLdagsljVlIHT9SWm_gJeVnIPnIjgd0h2t9UY2q_O87hUHMSyXnAy3oZ2LqsW6B4VOMFEzQphf2fumH7DBP5NLGh912E3hFPSajVVN1cCOWKMIK94sOXIUcjyX4drT0wGcdwkR8MSNaRFOoeLnLIPpYiJzMxW_rqbupktaspaZ735G4u2aHeDN46ZJyOSL8tjbEqBkysbCLiGlJ4Ju3WEv6dz4ByPeoEpkJZnmg'


class FatpenguinCastingTestCase(unittest.TestCase):
    def setUp(self):
        APP.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://castingagency:password12345@localhost:5432/castingagency-test"
        self.app = APP
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}

        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actors'], list)

    def test_get_actors_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actor'], dict)
        self.assertIsInstance(data['actor']['id'], int)
        self.assertEqual(data['actor']['name'], 'Jim Bob')
        self.assertEqual(data['actor']['gender'], 'male')
        self.assertEqual(data['actor']['date_of_birth'], '1950-01-01')
        self.assertIsInstance(data['actor']['movies'], list)

    def test_create_actor_missing_data(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_create_actor_invalid_date(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-61'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_create_actor_no_auth(self):
        res = self.client().post(
            '/actors',
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_actor_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        res = self.client().patch(
            f"/actors/{data['actor']['id']}",
            headers=self.headers,
            data=json.dumps({
                'name': 'Jane Bob',
                'gender': 'female',
                'date_of_birth': '1960-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actor'], dict)
        self.assertIsInstance(data['actor']['id'], int)
        self.assertEqual(data['actor']['name'], 'Jane Bob')
        self.assertEqual(data['actor']['gender'], 'female')
        self.assertEqual(data['actor']['date_of_birth'], '1960-01-01')
        self.assertIsInstance(data['actor']['movies'], list)

    def test_update_actor_no_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().patch(
            f"/actors/9999",
            headers=self.headers,
            data=json.dumps({
                'name': 'Jane Bob',
                'gender': 'female',
                'date_of_birth': '1960-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_actor_missing_data(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        res = self.client().patch(
            f"/actors/{data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_update_actor_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        res = self.client().patch(
            f"/actors/{data['actor']['id']}",
            data=json.dumps({
                'name': 'Jane Bob',
                'gender': 'female',
                'date_of_birth': '1960-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_actor_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().patch(
            f"/actors/{data['actor']['id']}",
            headers=self.headers,
            data=json.dumps({
                'name': 'Jane Bob',
                'gender': 'female',
                'date_of_birth': '1960-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        original_data = json.loads(res.data)

        res = self.client().delete(
            f"/actors/{original_data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], original_data['actor']['id'])

    def test_delete_actor_no_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().delete(
            f"/actors/9999",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        original_data = json.loads(res.data)

        res = self.client().delete(
            f"/actors/{original_data['actor']['id']}"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_actor_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        original_data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().delete(
            f"/actors/{original_data['actor']['id']}"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_movies(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movies'], list)

    def test_get_movies_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie'], dict)
        self.assertIsInstance(data['movie']['id'], int)
        self.assertEqual(data['movie']['title'], 'My best movie production')
        self.assertEqual(data['movie']['release_date'], '1950-01-01')
        self.assertIsInstance(data['movie']['actors'], list)

    def test_create_movie_missing_data(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_create_movie_no_auth(self):
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_movie_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().patch(
            f"/movies/{data['movie']['id']}",
            headers=self.headers,
            data=json.dumps({
                'title': 'My bestest movie production',
                'release_date': '1970-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie'], dict)
        self.assertIsInstance(data['movie']['id'], int)
        self.assertEqual(data['movie']['title'], 'My bestest movie production')
        self.assertEqual(data['movie']['release_date'], '1970-01-01')
        self.assertIsInstance(data['movie']['actors'], list)

    def test_update_movie_no_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().patch(
            f"/movies/9999",
            headers=self.headers,
            data=json.dumps({
                'title': 'My bestest movie production',
                'release_date': '1970-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_movie_missing_data(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        res = self.client().patch(
            f"/movies/{data['movie']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_update_movie_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        res = self.client().patch(
            f"/movies/{data['movie']['id']}",
            data=json.dumps({
                'title': 'My bestest movie production',
                'release_date': '1970-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_movie_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().patch(
            f"/movies/{data['movie']['id']}",
            headers=self.headers,
            data=json.dumps({
                'title': 'My bestest movie production',
                'release_date': '1970-01-01'
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        original_data = json.loads(res.data)

        res = self.client().delete(
            f"/movies/{original_data['movie']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], original_data['movie']['id'])

    def test_delete_movie_no_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().delete(
            f"/movies/9999",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movie_no_auth(self):
        res = self.client().delete(
            f"/movies/1",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_movie_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().delete(
            f"/movies/1",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(res.data)

        res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie'], dict)
        self.assertIsInstance(data['movie']['id'], int)
        self.assertEqual(data['movie']['title'], 'My best movie production')
        self.assertEqual(data['movie']['release_date'], '1950-01-01')
        self.assertIsInstance(data['movie']['actors'], list)
        self.assertIsInstance(data['movie']['actors'][0], dict)
        self.assertEqual(data['movie']['actors'][0]['name'], 'Jim Bob')
        self.assertEqual(data['movie']['actors'][0]
                         ['date_of_birth'], '1950-01-01')
        self.assertEqual(data['movie']['actors'][0]['gender'], 'male')

    def test_add_actor_to_movie_already_exists(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(res.data)

        res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(res.data)

        res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie_no_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(res.data)

        res = self.client().post(
            f"/movies/9999/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie_no_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(res.data)

        res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': 9999
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie_no_auth(self):
        res = self.client().post(
            f"/movies/1/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': 1
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        res = self.client().post(
            f"/movies/1/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': 1
            })
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(res.data)

        res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(res.data)

        res = self.client().delete(
            f"/movies/{movie_data['movie']['id']}/actors/{actor_data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], movie_data['movie']['id'])
        self.assertEqual(data['movie_id'], actor_data['actor']['id'])

    def test_delete_actor_from_movie_no_role(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        movie_res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(movie_res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        actor_res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(actor_res.data)

        actor2_res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'James Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor2_data = json.loads(actor2_res.data)

        add_role_res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        add_role_data = json.loads(add_role_res.data)

        res = self.client().delete(
            f"/movies/{movie_data['movie']['id']}/actors/{actor2_data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie_no_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        movie_res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(movie_res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        actor_res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(actor_res.data)

        add_role_res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        add_role_data = json.loads(add_role_res.data)

        res = self.client().delete(
            f"/movies/9999/actors/{actor_data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie_no_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        movie_res = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'My best movie production',
                'release_date': '1950-01-01'
            })
        )
        movie_data = json.loads(movie_res.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        actor_res = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jim Bob',
                'gender': 'male',
                'date_of_birth': '1950-01-01'
            })
        )
        actor_data = json.loads(actor_res.data)

        add_role_res = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        add_role_data = json.loads(add_role_res.data)

        res = self.client().delete(
            f"/movies/{movie_data['movie']['id']}/actors/9999",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie_no_auth(self):
        res = self.client().delete(
            f"/movies/1/actors/1",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie_forbidden(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )

        res = self.client().delete(
            f"/movies/1/actors/1",
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
