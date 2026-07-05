from app.services.product_import import ProductImportService


def test_import_extracts_product_metadata_from_html() -> None:
    html = """
    <html>
      <head>
        <title>Tailored Linen Blazer</title>
        <meta property="og:title" content="Tailored Linen Blazer" />
        <meta property="og:image" content="https://example.com/blazer.jpg" />
        <meta property="product:price:amount" content="89.99" />
        <script type="application/ld+json">
          {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Tailored Linen Blazer",
            "brand": {"@type": "Brand", "name": "Veloura House"},
            "image": "https://example.com/blazer.jpg",
            "color": "beige",
            "offers": {"@type": "Offer", "price": "89.99"}
          }
        </script>
      </head>
      <body></body>
    </html>
    """

    extracted = ProductImportService()._extract("https://example.com/blazer", html)

    assert extracted.title == "Tailored Linen Blazer"
    assert extracted.brand == "Veloura House"
    assert extracted.price == 89.99
    assert extracted.image_url == "https://example.com/blazer.jpg"
    assert extracted.color == "Beige"
    assert extracted.category and extracted.category.value == "tops"
