import uuid
from seller.dtos.seller_dto import SellerDTO

def test_seller_dto_from_dict(faker):
    data = {
        "user_id": str(uuid.uuid4()),
        "name": faker.name(),
        "phone": "+1234567890",
        "email": faker.email(),
        "zone": "NORTH",
        "quota_expected": 1000,
        "currency_quota": "USD",
        "quartely_target": 500,
        "currency_target": "USD",
        "performance_recomendations": "Keep up the good work!"
    }
    seller = SellerDTO.from_dict(data)
    assert seller.user_id == data['user_id']
    assert seller.name == data['name']
    assert seller.phone == data['phone']
    assert seller.email == data['email']
    assert seller.zone == data['zone']
    assert seller.quota_expected == data['quota_expected']
    assert seller.currency_quota == data['currency_quota']
    assert seller.quartely_target == data['quartely_target']
    assert seller.currency_target == data['currency_target']
    assert seller.performance_recomendations == data['performance_recomendations']
