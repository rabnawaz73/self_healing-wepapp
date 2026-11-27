"""Application route definitions."""
"""Application route definitions."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app import config


router = APIRouter()

PRODUCTS = [
    {"id": 1, "name": "Cloud Rescue Hoodie", "price": 49.99, "category": "Clothing"},
    {"id": 2, "name": "Incident Response Mug", "price": 18.50, "category": "Accessories"},
    {"id": 3, "name": "Monitoring Sticker Pack", "price": 9.99, "category": "Accessories"},
]


class OrderRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1, le=100)
    customer_name: str = Field(default="Guest", min_length=1, max_length=100)


@router.get("/", response_class=HTMLResponse)
def home() -> str:
    product_cards = "".join(
        f"""
        <article class="product-card">
          <div class="product-image" aria-hidden="true">CR</div>
          <div class="product-content">
            <span class="category">{product["category"]}</span>
            <h2>{product["name"]}</h2>
            <p class="price">${product["price"]:.2f}</p>
            <button type="button" onclick="placeOrder({product["id"]}, this)">Add to order</button>
          </div>
        </article>
        """
        for product in PRODUCTS
    )

    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{config.SERVICE_NAME}</title>
        <style>
          :root {{
            --ink: #10233a;
            --blue: #1769aa;
            --cyan: #21a6a1;
            --cream: #f4f7fb;
            --white: #ffffff;
          }}
          * {{ box-sizing: border-box; }}
          body {{
            margin: 0;
            min-height: 100vh;
            font-family: Inter, "Segoe UI", sans-serif;
            color: var(--ink);
            background: linear-gradient(135deg, #eef4f8 0%, #f9fbfd 100%);
          }}
          nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px max(24px, 7vw);
            background: rgba(255, 255, 255, 0.92);
            border-bottom: 1px solid #dde7ef;
          }}
          .brand {{ font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }}
          .brand span {{ color: var(--cyan); }}
          .status {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #39705e;
            background: #eaf7f2;
            border-radius: 999px;
            padding: 8px 12px;
            font-size: 13px;
            font-weight: 700;
          }}
          .status::before {{
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #27ae60;
            box-shadow: 0 0 0 4px rgba(39, 174, 96, 0.12);
          }}
          main {{ max-width: 1120px; margin: 0 auto; padding: 64px 24px 80px; }}
          .hero {{
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 24px;
            align-items: end;
            margin-bottom: 42px;
          }}
          .eyebrow {{ color: var(--cyan); font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }}
          h1 {{ max-width: 700px; margin: 12px 0; font-size: clamp(44px, 7vw, 78px); line-height: 0.98; }}
          .hero p {{ max-width: 520px; color: #5a6c7d; font-size: 18px; line-height: 1.7; }}
          .release {{
            justify-self: end;
            min-width: 220px;
            padding: 20px;
            border-radius: 16px;
            background: var(--ink);
            color: white;
            box-shadow: 0 18px 45px rgba(16, 35, 58, 0.18);
          }}
          .release small {{ color: #aebdcb; }}
          .release strong {{ display: block; margin-top: 8px; font-size: 24px; }}
          .products {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
          .product-card {{
            overflow: hidden;
            border: 1px solid #dde7ef;
            border-radius: 18px;
            background: var(--white);
            box-shadow: 0 12px 30px rgba(38, 65, 88, 0.08);
          }}
          .product-image {{
            display: grid;
            place-items: center;
            height: 150px;
            color: white;
            font-size: 42px;
            font-weight: 900;
            background: linear-gradient(135deg, var(--blue), var(--cyan));
          }}
          .product-content {{ padding: 20px; }}
          .category {{ color: var(--cyan); font-size: 12px; font-weight: 800; text-transform: uppercase; }}
          .product-content h2 {{ min-height: 52px; margin: 8px 0; font-size: 18px; }}
          .price {{ font-size: 22px; font-weight: 800; }}
          button {{
            width: 100%;
            border: 0;
            border-radius: 10px;
            padding: 12px;
            color: white;
            background: var(--ink);
            cursor: pointer;
            font-weight: 800;
          }}
          button:hover {{ background: var(--blue); }}
          #notice {{
            position: fixed;
            right: 24px;
            bottom: 24px;
            max-width: 320px;
            padding: 14px 18px;
            border-radius: 10px;
            color: white;
            background: var(--ink);
            opacity: 0;
            transform: translateY(12px);
            transition: 0.2s ease;
          }}
          #notice.visible {{ opacity: 1; transform: translateY(0); }}
          @media (max-width: 760px) {{
            .hero {{ grid-template-columns: 1fr; }}
            .release {{ justify-self: start; }}
            .products {{ grid-template-columns: 1fr; }}
          }}
        </style>
      </head>
      <body>
        <nav>
          <div class="brand">Cloud<span>Rescue</span></div>
          <div class="status">System healthy</div>
        </nav>
        <main>
          <section class="hero">
            <div>
              <div class="eyebrow">Deployment resilience</div>
              <h1>Built to recover.</h1>
              <p>A self-healing cloud storefront designed to detect failed releases, preserve the last healthy deployment, and keep service available.</p>
            </div>
            <aside class="release">
              <small>Active release</small>
              <strong>v{config.APP_VERSION}</strong>
              <small>{config.ENVIRONMENT}</small>
            </aside>
          </section>
          <section class="products" aria-label="Products">{product_cards}</section>
        </main>
        <div id="notice" role="status"></div>
        <script>
          async function placeOrder(productId, button) {{
            button.disabled = true;
            button.textContent = "Adding...";
            const response = await fetch("/orders", {{
              method: "POST",
              headers: {{"Content-Type": "application/json"}},
              body: JSON.stringify({{product_id: productId, quantity: 1, customer_name: "Guest"}})
            }});
            const result = await response.json();
            const notice = document.getElementById("notice");
            notice.textContent = response.ok ? "Order " + result.order_id + " created" : "Order could not be created";
            notice.classList.add("visible");
            button.disabled = false;
            button.textContent = "Add to order";
            setTimeout(() => notice.classList.remove("visible"), 3000);
          }}
        </script>
      </body>
    </html>
    """


@router.get("/health")
def health() -> dict:
    if config.FORCE_UNHEALTHY:
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy",
            "version": config.APP_VERSION,
            "service": config.SERVICE_NAME,
        })

    return {
        "status": "healthy",
        "version": config.APP_VERSION,
        "service": config.SERVICE_NAME,
    }


@router.get("/version")
def version() -> dict:
    return {
        "version": config.APP_VERSION,
        "environment": config.ENVIRONMENT,
    }


@router.get("/products")
def products() -> dict:
    return {"products": PRODUCTS, "count": len(PRODUCTS)}


@router.post("/orders")
def create_order(order: OrderRequest) -> dict:
    product = next((item for item in PRODUCTS if item["id"] == order.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "order_id": f"CR-{order.product_id}-{order.quantity:04d}",
        "product": product,
        "quantity": order.quantity,
        "customer_name": order.customer_name,
        "total": round(product["price"] * order.quantity, 2),
        "status": "created",
    }
