from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


SORT_OPTIONS = {
    "name_asc": Product.name.asc(),
    "name_desc": Product.name.desc(),
    "price_asc": Product.price.asc(),
    "price_desc": Product.price.desc(),
    "stock_asc": Product.current_stock.asc(),
    "stock_desc": Product.current_stock.desc(),
    "newest": Product.created_at.desc(),
    "oldest": Product.created_at.asc(),
}


def get_products(
    db: Session,
    search: Optional[str] = None,
    category: Optional[str] = None,
    low_stock_only: bool = False,
    sort: Optional[str] = None,
) -> list[Product]:
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search.strip()}%"))

    if category:
        query = query.filter(Product.category.ilike(category.strip()))

    if low_stock_only:
        query = query.filter(Product.current_stock <= Product.minimum_stock)

    order_by = SORT_OPTIONS.get(sort or "name_asc", Product.name.asc())
    return query.order_by(order_by).all()


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    db: Session,
    product: Product,
    product_data: ProductUpdate,
) -> Product:
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def get_categories(db: Session) -> list[str]:
    rows = db.query(Product.category).distinct().order_by(Product.category.asc()).all()
    return [row[0] for row in rows]


def get_dashboard_stats(db: Session) -> dict:
    total_products = db.query(func.count(Product.id)).scalar() or 0
    low_stock_products = (
        db.query(func.count(Product.id))
        .filter(Product.current_stock <= Product.minimum_stock)
        .scalar()
        or 0
    )
    total_categories = db.query(func.count(func.distinct(Product.category))).scalar() or 0
    recent_products = (
        db.query(Product).order_by(Product.created_at.desc()).limit(5).all()
    )

    return {
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "total_categories": total_categories,
        "recent_products": recent_products,
    }


def seed_sample_data(db: Session) -> None:
    if db.query(Product).count() > 0:
        return

    sample_products = [
        Product(
            name="Wireless Mouse",
            description="Ergonomic wireless mouse with USB receiver.",
            category="Electronics",
            price=24.99,
            current_stock=45,
            minimum_stock=10,
        ),
        Product(
            name="Notebook A5",
            description="Ruled notebook with 120 pages.",
            category="Stationery",
            price=5.50,
            current_stock=8,
            minimum_stock=15,
        ),
        Product(
            name="USB-C Cable",
            description="2m braided USB-C charging cable.",
            category="Electronics",
            price=12.00,
            current_stock=3,
            minimum_stock=5,
        ),
        Product(
            name="Desk Lamp",
            description="LED desk lamp with adjustable brightness.",
            category="Furniture",
            price=35.00,
            current_stock=12,
            minimum_stock=5,
        ),
        Product(
            name="Ballpoint Pen Pack",
            description="Pack of 10 blue ballpoint pens.",
            category="Stationery",
            price=3.25,
            current_stock=50,
            minimum_stock=20,
        ),
    ]

    db.add_all(sample_products)
    db.commit()
