import json
import os
import uuid

import requests_mock

from stocks_api.config.cache import cache
from stocks_api.config.db import db
from stocks_api.models.stock_model import Stock

products_path = os.getenv('PRODUCTS_PATH', default='http://localhost:3017')


def test_unauthorized_access(client):
    response = client.get('/stocks-api/stocks/all', headers={'Content-Type': 'application/json'})
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.get('/stocks-api/stocks/all', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_get_stocks_success(client, headers, create_test_stocks):
    with requests_mock.Mocker() as m:
        m.post(f'{products_path}/products/by-ids', headers=headers, json=[])
        response = client.get('/stocks-api/stocks/all', headers=headers)
        response_data = json.loads(response.data)
        data = response_data['stocks']

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 10  # default per_page
    assert all(isinstance(item['id'], str) for item in data)
    assert all(isinstance(item['id_store'], str) for item in data)
    assert all(isinstance(item['id_product'], str) for item in data)
    assert all(isinstance(item['quantity_in_stock'], int) for item in data)
    assert all(isinstance(item['product'], dict) for item in data)
    assert response_data['total'] == 15
    assert response_data['page'] == 1
    assert response_data['per_page'] == 10


def test_get_stocks_pagination(client, headers, create_test_stocks):
    with requests_mock.Mocker() as m:
        m.post(f'{products_path}/products/by-ids', headers=headers, json=[])
        response = client.get('/stocks-api/stocks/all?page=2&per_page=5', headers=headers)
        response_data = json.loads(response.data)
        data = response_data['stocks']

    assert response.status_code == 200
    assert len(data) == 5
    assert isinstance(data[0]['id_product'], str)


def test_get_stocks_cache(client, headers, create_test_stocks):
    with requests_mock.Mocker() as m:
        m.post(f'{products_path}/products/by-ids', headers=headers, json=[])
        response1 = client.get('/stocks-api/stocks/all', headers=headers)
        response_data1 = json.loads(response1.data)
        data1 = response_data1['stocks']

        cache_key = f"stock:{data1[0]['id']}"
        cache.set(cache_key, json.dumps({'id': data1[0]['id'], 'quantity_in_stock': 999}))

        response2 = client.get('/stocks-api/stocks/all', headers=headers)
        response_data2 = json.loads(response2.data)
        data2 = response_data2['stocks']

    assert data2[0]['quantity_in_stock'] == 999
    assert data2[0]['id'] == data1[0]['id']


def test_get_stocks_invalid_pagination(client, headers, create_test_stocks):
    with requests_mock.Mocker() as m:
        m.post(f'{products_path}/products/by-ids', headers=headers, json=[])
        response = client.get('/stocks-api/stocks/all?page=0&per_page=100', headers=headers)
        response_data = json.loads(response.data)
        data = response_data['stocks']

    assert response.status_code == 200
    assert len(data) <= 50  # Should be capped at 50


def test_get_stocks_by_ids_missing(client, headers, create_test_stocks):
    response = client.post('/stocks-api/stocks/by-ids', headers=headers, json={})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'ids is required'


def test_get_stocks_by_ids_wrong(client, headers, create_test_stocks):
    response = client.post('/stocks-api/stocks/by-ids', headers=headers, json={'ids': {}})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'ids must be a list'


def test_get_stocks_by_ids_empty(client, headers, create_test_stocks):
    response = client.post('/stocks-api/stocks/by-ids', headers=headers, json={'ids': []})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'ids cannot be empty'


def test_get_stocks_by_ids_invalid(client, headers, create_test_stocks):
    response = client.post('/stocks-api/stocks/by-ids', headers=headers, json={'ids': [
        'invalid_id'
    ]})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'invalids product ids'


def test_get_stocks_by_ids_success(client, headers, create_test_stocks):
    stock_id_one = uuid.uuid4()
    stock_one = Stock(id=stock_id_one, id_product=uuid.uuid4(), id_store=uuid.uuid4(), quantity_in_stock=100,
                      last_quantity=100, enabled=True)
    db.session.add(stock_one)
    stock_id_two = uuid.uuid4()
    stock_two = Stock(id=stock_id_two, id_product=uuid.uuid4(), id_store=uuid.uuid4(), quantity_in_stock=200,
                      last_quantity=200, enabled=True)
    db.session.add(stock_two)
    db.session.commit()

    with requests_mock.Mocker() as m:
        m.post(f'{products_path}/products/by-ids', json=[
            {'id': str(stock_one.product_id), 'name': 'Product One'},
            {'id': str(stock_two.product_id), 'name': 'Product Two'}
        ], status_code=200)

        response_ids = client.post('/stocks-api/stocks/by-ids', headers=headers,
                                   json={"ids": [stock_id_one, stock_id_two]})
        data_ids = json.loads(response_ids.data)

    assert response_ids.status_code == 200
    assert len(data_ids) == 2
    assert data_ids[0]['id'] == str(stock_id_one)
    assert data_ids[0]['product']['name'] == 'Product One'
    assert data_ids[1]['id'] == str(stock_id_two)
    assert data_ids[1]['product']['name'] == 'Product Two'
    

def test_get_stocks_by_ids_http_products_fail(client, headers, create_test_stocks):
    stock_id_one = uuid.uuid4()
    stock_one = Stock(id=stock_id_one, product_id=uuid.uuid4(), store_id=uuid.uuid4(), quantity_in_stock=100,
                      last_quantity=100, enabled=True)
    db.session.add(stock_one)
    stock_id_two = uuid.uuid4()
    stock_two = Stock(id=stock_id_two, product_id=uuid.uuid4(), store_id=uuid.uuid4(), quantity_in_stock=200,
                      last_quantity=200, enabled=True)
    db.session.add(stock_two)
    db.session.commit()

    with requests_mock.Mocker() as m:
        m.post(f'{products_path}/products/by-ids', json=[], status_code=404)
        response_ids = client.post('/stocks-api/stocks/by-ids', headers=headers,
                                   json={"ids": [stock_id_one, stock_id_two]})
        data_ids = json.loads(response_ids.data)

    assert response_ids.status_code == 404
    assert data_ids['message'] == 'products not found'
    

def test_assign_stock_to_store_success(client, headers, create_test_stocks):
    
    data = {
        "store_id": "ca2b8eb4-431d-4abf-8afe-96f687890dac",
        "stocks" : [
            {
                "id" : "",
                "product_id" : "d707e529-3b7c-44ab-bac5-97b926889eba",
                "assigned_stock" : "120"
            }
        ]
    }

    response = client.put('/stocks-api/stocks/assign-stock-store', headers=headers, json=data)
    data_response = json.loads(response.data)

    assert response.status_code == 200
    assert data_response['message'] == 'Stocks assigned successfully'

def test_assign_stock_to_store_invalid(client, headers, create_test_stocks):
    
    data = {
        "store_id": "ca2b8eb4-431d-4abf-8afe-96f687890dac",
        "stocks" : [
            {
                "id" : "",
                "product_id" : "",
                "assigned_stock" : ""
            }
        ]
    }

    response = client.put('/stocks-api/stocks/assign-stock-store', headers=headers, json=data)
    data_response = json.loads(response.data)

    assert response.status_code == 400
    assert data_response['message'] == 'Error: Invalid product or stock data'

def test_assign_stock_to_store_update(client, headers, create_test_stocks):
    
    stock_id_one = uuid.uuid4()
    id_store = uuid.uuid4()
    id_product = uuid.uuid4()
    stock_one = Stock(id=stock_id_one, id_store=id_store, id_product=id_product, quantity_in_stock=100, last_quantity=100,
                      enabled=True)
    db.session.add(stock_one)
    db.session.commit()

    data = {
        "store_id": id_store,
        "stocks" : [
            {
                "id" : stock_id_one,
                "product_id" : id_product,
                "assigned_stock" : "120"
            }
        ]
    }

    response = client.put('/stocks-api/stocks/assign-stock-store', headers=headers, json=data)
    data_response = json.loads(response.data)

    # Verifying the stock was updated in the database
    updated_stock = Stock.query.get(stock_id_one)


    assert response.status_code == 200
    assert data_response['message'] == 'Stocks assigned successfully'
    assert updated_stock.quantity_in_stock == 120

def test_get_stock_by_store_id(client, headers, create_test_stocks):
    store_id = uuid.uuid4()
    stock_id_one = uuid.uuid4()
    id_product = uuid.uuid4()
    stock_one = Stock(id=stock_id_one, id_store=store_id, id_product=id_product, quantity_in_stock=100, last_quantity=100,
                      enabled=True)
    db.session.add(stock_one)
    db.session.commit()

    response = client.get(f'/stocks-api/stocks/by-store-id?id_store={str(store_id)}', headers=headers)
    data_response = json.loads(response.data)

    assert response.status_code == 200
    assert len(data_response) == 2
    assert data_response['id_store'] == str(store_id)
