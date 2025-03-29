import uuid
from seller.models.seller_model import Seller, SELLER_ZONE, CURRENCY

def test_seller_model_creation(faker):
    seller = Seller(
        user_id=uuid.uuid4(),
        name=faker.name(),
        phone="+1" + faker.numerify("#" * 10),
        email=faker.email(),
        zone=SELLER_ZONE.CENTER,
        quota_expected=faker.pyfloat(min_value=1000, max_value=10000),
        currency_quota=CURRENCY.USD,
        quartely_target=faker.pyfloat(min_value=5000, max_value=50000),
        currency_target=CURRENCY.USD,
        performance_recomendations=faker.sentence()
    )
    
    assert seller.name is not None
    assert seller.email is not None
    assert seller.zone == SELLER_ZONE.CENTER
    assert seller.quota_expected > 0
    assert seller.quartely_target > 0
