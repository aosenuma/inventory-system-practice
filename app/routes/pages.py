from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import ProductCreate, ProductUpdate

router = APIRouter(tags=["Pages"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _parse_form_product(
    name: str,
    description: str,
    category: str,
    price: float,
    current_stock: int,
    minimum_stock: int,
) -> ProductCreate:
    return ProductCreate(
        name=name,
        description=description or None,
        category=category,
        price=price,
        current_stock=current_stock,
        minimum_stock=minimum_stock,
    )


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "stats": stats,
            "recent_products": stats["recent_products"],
        },
    )


@router.get("/products", response_class=HTMLResponse)
def products_list(
    request: Request,
    search: str | None = None,
    category: str | None = None,
    low_stock: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    low_stock_only = low_stock == "1"
    selected_sort = sort if sort in crud.SORT_OPTIONS else "name_asc"
    products = crud.get_products(
        db,
        search=search,
        category=category,
        low_stock_only=low_stock_only,
        sort=selected_sort,
    )
    categories = crud.get_categories(db)

    return templates.TemplateResponse(
        request=request,
        name="products/index.html",
        context={
            "products": products,
            "categories": categories,
            "search": search or "",
            "selected_category": category or "",
            "low_stock_only": low_stock_only,
            "selected_sort": selected_sort,
        },
    )


@router.get("/products/create", response_class=HTMLResponse)
def product_create_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products/create.html",
        context={"errors": None, "form_data": {}},
    )


@router.post("/products/create")
def product_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    category: str = Form(...),
    price: float = Form(...),
    current_stock: int = Form(...),
    minimum_stock: int = Form(...),
    db: Session = Depends(get_db),
):
    form_data = {
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "current_stock": current_stock,
        "minimum_stock": minimum_stock,
    }

    try:
        product_data = _parse_form_product(**form_data)
        crud.create_product(db, product_data)
        return RedirectResponse(url="/products?success=created", status_code=303)
    except ValidationError as exc:
        errors = [err["msg"] for err in exc.errors()]
        return templates.TemplateResponse(
            request=request,
            name="products/create.html",
            context={"errors": errors, "form_data": form_data},
            status_code=400,
        )


@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        request=request,
        name="products/detail.html",
        context={"product": product},
    )


@router.get("/products/{product_id}/edit", response_class=HTMLResponse)
def product_edit_form(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        request=request,
        name="products/edit.html",
        context={"product": product, "errors": None},
    )


@router.post("/products/{product_id}/edit")
def product_edit(
    product_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    category: str = Form(...),
    price: float = Form(...),
    current_stock: int = Form(...),
    minimum_stock: int = Form(...),
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        product_data = ProductUpdate(
            name=name,
            description=description or None,
            category=category,
            price=price,
            current_stock=current_stock,
            minimum_stock=minimum_stock,
        )
        crud.update_product(db, product, product_data)
        return RedirectResponse(
            url=f"/products/{product_id}?success=updated",
            status_code=303,
        )
    except ValidationError as exc:
        errors = [err["msg"] for err in exc.errors()]
        return templates.TemplateResponse(
            request=request,
            name="products/edit.html",
            context={"product": product, "errors": errors},
            status_code=400,
        )


@router.post("/products/{product_id}/delete")
def product_delete(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.delete_product(db, product)
    return RedirectResponse(url="/products?success=deleted", status_code=303)
