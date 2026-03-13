import pytest
from eapp.test.test_base import create_app, test_app, test_session
from eapp import db
from eapp.dao import Product
from eapp.dao import load_products

@pytest.fixture
def sample_products(test_session):
    p1 = Product(name="Iphone 69", price=36, category_id=1)
    p2 = Product(name="Samsung Galaxy 69", price=27, category_id=1)
    p3 = Product(name="Iphone 6s", price=67, category_id=2)
    p4 = Product(name="Xiaomi 69", price=91, category_id=2)

    samples = [ p1, p2, p3, p4 ]
    db.session.add_all(samples)
    db.session.commit()

    return samples

def test_create_product(sample_products):
    samples = load_products()
    
    assert len(samples) == len(sample_products)

def test_search_product_cate_id(sample_products):
    cate_id = 1
    actual_prods = load_products(cate_id=cate_id)

    assert len(actual_prods) == 2
    assert all(p.category_id == cate_id for p in actual_prods)

def test_search_product_kw(sample_products):
    kw = "Iphone"
    actual_prods = load_products(kw=kw)

    assert len(actual_prods) == 2
    assert all(kw in p.name for p in actual_prods)

def test_search_kw_cate(sample_products):
    kw = "Iphone"
    cate_id = 2
    actual_prods = load_products(kw=kw, cate_id=cate_id)

    assert len(actual_prods) == 1
    assert kw in actual_prods[0].name
    assert cate_id == actual_prods[0].category_id

@pytest.mark.parametrize("x, expected", [
    (2, ["Iphone 6s", "Xiaomi 69"]),
    (1, ['Iphone 69', "Samsung Galaxy 69"]),
    (-1, ['Iphone 69', "Samsung Galaxy 69", "Iphone 6s", "Xiaomi 69"]),
    (None, ['Iphone 69', "Samsung Galaxy 69", "Iphone 6s", "Xiaomi 69"]),
])
def test_search_paging(test_app, sample_products, x, expected):
    actual_prods = load_products(page=x)
    assert all(expected[i] == p.name for i, p in enumerate(actual_prods))

