import json
from tests.BaseCase import BaseCase
from database.mortgage_rate import range_700_759
from database.pmi import downpayment_zero, downpayment_five, downpayment_ten, downpayment_fifteen


class TestAuthorization(BaseCase):
    def test_get_report_by_user(self):
    # Post for mortgage_rate
        self.app.post('/api/v1/mortgage-rate', headers={"Content-Type":"application/json"}, data=json.dumps(range_700_759))
    # Post for pmi
        self.app.post('/api/v1/pmi', headers={"Content-Type":"application/json"}, data=json.dumps(downpayment_zero))
        self.app.post('/api/v1/pmi', headers={"Content-Type":"application/json"}, data=json.dumps(downpayment_five))
        self.app.post('/api/v1/pmi', headers={"Content-Type":"application/json"}, data=json.dumps(downpayment_ten))
        self.app.post('/api/v1/pmi', headers={"Content-Type":"application/json"}, data=json.dumps(downpayment_fifteen))
    #Given
        harry_uid = { "uid": 'jhdfs783uy4ir98f7ygh2jeuwidsi8943yrih' }

        harry_report = {
            "zipcode": 80209,
            "credit_score": 710,
            "salary": 5000,
            "monthly_debt": 1500,
            "downpayment_savings": 50000,
            "mortgage_term": 30,
            "downpayment_percentage": 19,
            "goal_principal": 500000,
            "rent": 0,
            "uid": harry_uid['uid']
        }
        self.app.post('/api/v1/report', headers={"Content-Type": "application/json"}, data=json.dumps(harry_report))

        ginny_uid = { "uid": 'bdj857ytwgyurf897yughjjjw98d7yugh4b3ei' }
        ginny_report = {
            "zipcode": 80209,
            "credit_score": 720,
            "salary": 8000,
            "monthly_debt": 2500,
            "downpayment_savings": 60000,
            "mortgage_term": 30,
            "downpayment_percentage": 10,
            "goal_principal": 600000,
            "rent": 0,
            "uid": ginny_uid['uid']
        }
        self.app.post('/api/v1/report', headers={"Content-Type": "application/json"}, data=json.dumps(ginny_report))
    # When
        harry_response = self.app.post('/api/v1/report/unique', headers={"Content-Type": "application/json"}, data=json.dumps(harry_uid))
        harry_data = harry_response.json['data']
    # Then
        self.assertEqual(200, harry_response.status_code)
        self.assertEqual(harry_report['credit_score'], harry_data['03_attributes']['input']['B_credit_score'])
        self.assertNotEqual(ginny_report['credit_score'], harry_data['03_attributes']['input']['B_credit_score'])
    # When

        ginny_response = self.app.post('/api/v1/report/unique', headers={"Content-Type": "application/json"}, data=json.dumps(ginny_uid))
        ginny_data = ginny_response.json['data']
    # Then
        self.assertEqual(200, ginny_response.status_code)
        self.assertEqual(ginny_report['credit_score'], ginny_data['03_attributes']['input']['B_credit_score'])
        self.assertNotEqual(harry_report['credit_score'], ginny_data['03_attributes']['input']['B_credit_score'])

    def test_user_wants_to_register(self):
    # Post for mortgage_rate
        self.app.post('/api/v1/mortgage-rate', headers={"Content-Type":"application/json"}, data=json.dumps(range_700_759))
    # Given
        unregistered_report = {
            "zipcode": 80209,
            "credit_score": 710,
            "salary": 5000,
            "monthly_debt": 1500,
            "downpayment_savings": 50000,
            "mortgage_term": 30,
            "downpayment_percentage": 20,
            "goal_principal": 500000,
            "rent": 0
        }

        response = self.app.post('/api/v1/report', headers={"Content-Type": "application/json"}, data=json.dumps(unregistered_report))
        data = response.json['data']
        id = data['id']
        url = data['confirmation']['url']
        unregistered_confirmation = self.app.get(url, headers={"Content-Type": "application/json"})
    # When
        user_payload = {
            "uid": 'asefiojoidfcjcoiaswe4freowi4'
        }

        updated_response = self.app.put(f'/api/v1/report/{id}', headers={"Content-Type": "application/json"}, data=json.dumps(user_payload))
        updated_data = updated_response.json['data']

        registered_confirmation = self.app.post('/api/v1/report/unique', headers={"Content-Type": "application/json"}, data=json.dumps(user_payload))
    #Then
        self.assertEqual(200, registered_confirmation.status_code)
        self.assertEqual(unregistered_confirmation.json, registered_confirmation.json)

    def test_user_wants_to_register_sad_path_missing_uid(self):
    # Post for mortgage_rate
        self.app.post('/api/v1/mortgage-rate', headers={"Content-Type":"application/json"}, data=json.dumps(range_700_759))
    # Given
        unregistered_report = {
            "zipcode": 80209,
            "credit_score": 710,
            "salary": 5000,
            "monthly_debt": 1500,
            "downpayment_savings": 50000,
            "mortgage_term": 30,
            "downpayment_percentage": 20,
            "goal_principal": 500000,
            "rent": 0
        }

        response = self.app.post('/api/v1/report', headers={"Content-Type": "application/json"}, data=json.dumps(unregistered_report))

    # When


        error_confirmation = self.app.post('/api/v1/report/unique', headers={"Content-Type": "application/json"})
    #Then
        data = error_confirmation.json['data']
        self.assertEqual(410, data['error'])
        self.assertEqual("Missing UID", data['message'])

    def test_registered_user_sad_path_wrong_uid(self):
    # Post for mortgage_rate
        self.app.post('/api/v1/mortgage-rate', headers={"Content-Type":"application/json"}, data=json.dumps(range_700_759))
    # Given
        registered_report = {
            "zipcode": 80209,
            "credit_score": 710,
            "salary": 5000,
            "monthly_debt": 1500,
            "downpayment_savings": 50000,
            "mortgage_term": 30,
            "downpayment_percentage": 20,
            "goal_principal": 500000,
            "rent": 0,
            "uid": 'wsorefijcocetijvspowq2p'
        }

        response = self.app.post('/api/v1/report', headers={"Content-Type": "application/json"}, data=json.dumps(registered_report))

    # When
        wrong_uid = {"uid": 'awdorfnjcaoielruwbn'}
        error_confirmation = self.app.post('/api/v1/report/unique', headers={"Content-Type": "application/json"}, data=json.dumps(wrong_uid))
    #Then
        data = error_confirmation.json['data']
        self.assertEqual(406, data['error'])
        self.assertEqual("No report matches this user", data['message'])
