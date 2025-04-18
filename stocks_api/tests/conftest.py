import os
import uuid
import pytest
import uuid

from stocks_api import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app
    from stocks_api.config.db import db
    db.session.rollback()
    db.session.close()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def headers():
    return {
        'x-token': os.getenv('INTERNAL_TOKEN', default='internal_token'),
        'Content-Type': 'application/json'
    }


@pytest.fixture
def create_test_stocks(app):
    from stocks_api.config.db import db
    from stocks_api.models.stock_model import Stock
    
    id_store = uuid.uuid4()

    stocks = []
    for i in range(15):
        stock = Stock(
            id_product=uuid.uuid4(),
            id_store=id_store,
            quantity_in_stock=100 + i,
            last_quantity=100 + i,
            enabled=True
        )
        stocks.append(stock)

    with app.app_context():
        db.session.bulk_save_objects(stocks)
        db.session.commit()

    return stocks
