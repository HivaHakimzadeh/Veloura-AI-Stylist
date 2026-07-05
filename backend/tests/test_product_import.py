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


def test_import_normalizes_amazon_tracking_url() -> None:
    service = ProductImportService()
    tracking_url = (
        "https://www.amazon.com/sspa/click?url=%2FVan-Cleef-Necklace-Women%2Fdp%2FB000TEST12"
        "%2Fref%3Dsr_1_2_sspa&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY"
    )

    normalized = service._normalize_product_url(tracking_url)
    fallback = service._fallback_extract(normalized)

    assert normalized == "https://www.amazon.com/van-cleef-necklace-women/dp/B000TEST12"
    assert fallback.title == "Van Cleef Necklace Women"
    assert fallback.brand == "Amazon"


def test_import_extracts_amazon_price_and_image_from_html() -> None:
    html = """
    <html>
      <head>
        <title>Billet-doux 18k Gold Plated Clover Necklace</title>
      </head>
      <body>
        <img
          id="landingImage"
          src="https://m.media-amazon.com/images/I/61TXMZTwEWL._AC_SY300_SX300_QL70_ML2_.jpg"
          data-a-dynamic-image='{"https://m.media-amazon.com/images/I/61TXMZTwEWL._AC_SY695_.jpg":[695,692]}'
        />
        <div id="corePriceDisplay_desktop_feature_div">
          <span class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay apex-pricetopay-value">
            <span class="a-offscreen">$16.99</span>
          </span>
        </div>
      </body>
    </html>
    """

    extracted = ProductImportService()._extract(
        "https://www.amazon.com/Billet-doux-Necklace-Valentines-Four-Leaf-Adjustable/dp/B0FT9WWXGY",
        html,
    )

    assert extracted.price == 16.99
    assert extracted.image_url.startswith("https://m.media-amazon.com/images/I/61TXMZTwEWL")
