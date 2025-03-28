import uuid
import pytest
from seller.infrastructure.seller_repository import SellerRepository
from seller.models.seller_model import Seller, SELLER_ZONE, CURRENCY

@pytest.fixture
def repo(db_session):
    return SellerRepository(db_session)

def test_create_and_get_seller(repo, db_session, faker):
    seller_data = {
        "user_id": str(uuid.uuid4()),
        "name": faker.name(),
        "phone": "+1" + faker.numerify("#" * 10),
        "email": faker.email(),
        "zone": SELLER_ZONE.CENTER.value,
        "quota_expected": faker.pyfloat(min_value=1000, max_value=10000),
        "currency_quota": CURRENCY.USD.value,
        "quartely_target": faker.pyfloat(min_value=5000, max_value=50000),
        "currency_target": CURRENCY.USD.value,
        "performance_recomendations": faker.sentence()
    }
    
    # Create a seller using the repository
    seller = repo.create_seller(seller_data)
    db_session.commit()

    fetched_seller = repo.get_seller_by_user_id(seller.user_id)
    assert fetched_seller is not None
    assert fetched_seller.email == seller_data['email']
    assert fetched_seller.zone == SELLER_ZONE.CENTER
    assert fetched_seller.currency_quota == CURRENCY.USD
