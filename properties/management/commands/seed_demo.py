"""
Seeds the database with a demo agent, a demo client, and a handful of
sample properties (with generated placeholder images) so the app has
something to look at immediately after setup.

Usage:
    python manage.py seed_demo
"""
import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from properties.models import Property
from transactions.models import Transaction

User = get_user_model()

DEMO_PROPERTIES = [
    {
        "title": "Sunrise Residency 2BHK",
        "description": "A bright, well-ventilated 2BHK apartment on the 4th floor with a balcony "
                        "overlooking a landscaped garden. Close to schools, metro, and shopping.",
        "listing_type": "sale",
        "price": 6500000,
        "address": "100 Feet Road",
        "city": "Indiranagar, Bengaluru",
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 1150,
        "color": (184, 134, 59),
    },
    {
        "title": "Whitefield Tech Park View 3BHK",
        "description": "Spacious 3BHK in a gated community, walking distance to major IT parks. "
                        "Modular kitchen, covered parking, and 24/7 security.",
        "listing_type": "rent",
        "price": 42000,
        "address": "ITPL Main Road",
        "city": "Whitefield, Bengaluru",
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 1600,
        "color": (20, 33, 61),
    },
    {
        "title": "HSR Layout Compact 1BHK",
        "description": "Cozy 1BHK ideal for a small family or working professional. Newly painted, "
                        "with a dedicated parking spot and close to Sector 2 market.",
        "listing_type": "rent",
        "price": 21000,
        "address": "27th Main",
        "city": "HSR Layout, Bengaluru",
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqft": 650,
        "color": (69, 82, 107),
    },
    {
        "title": "Koramangala Duplex Villa",
        "description": "Premium 4BHK duplex villa with a private terrace garden, home office space, "
                        "and two dedicated parking bays in a quiet, tree-lined street.",
        "listing_type": "sale",
        "price": 21000000,
        "address": "5th Block",
        "city": "Koramangala, Bengaluru",
        "bedrooms": 4,
        "bathrooms": 4,
        "area_sqft": 3200,
        "color": (143, 102, 38),
    },
    {
        "title": "Jayanagar Family Home 3BHK",
        "description": "Classic South Bengaluru home close to Jayanagar 4th Block market, with a "
                        "private garden and traditional layout. Great for a growing family.",
        "listing_type": "sale",
        "price": 12500000,
        "address": "4th Block",
        "city": "Jayanagar, Bengaluru",
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 1900,
        "color": (31, 122, 77),
    },
    {
        "title": "Electronic City Starter 2BHK",
        "description": "Affordable, well-maintained 2BHK close to Electronic City Phase 1, ideal for "
                        "young professionals commuting to nearby tech campuses.",
        "listing_type": "rent",
        "price": 18000,
        "address": "Hosur Road",
        "city": "Electronic City, Bengaluru",
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 980,
        "color": (30, 74, 138),
    },
]


def generate_placeholder_image(title, color):
    """Generate a simple 800x500 placeholder image with the property title on it."""
    from PIL import Image, ImageDraw, ImageFont

    width, height = 800, 500
    img = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(img)

    # Subtle diagonal accent stripe
    overlay_color = tuple(min(255, c + 25) for c in color)
    draw.polygon(
        [(0, height), (width * 0.55, height), (width * 0.85, 0), (width * 0.55, 0)],
        fill=overlay_color,
    )

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
        small_font = font

    # Word-wrap the title across up to 2 lines
    words = title.split()
    lines, current = [], ""
    for w in words:
        trial = (current + " " + w).strip()
        if draw.textlength(trial, font=font) > width - 80 and current:
            lines.append(current)
            current = w
        else:
            current = trial
    if current:
        lines.append(current)

    y = height / 2 - (len(lines) * 42) / 2
    for line in lines:
        draw.text((40, y), line, font=font, fill="white")
        y += 42

    draw.text((40, height - 50), "Demo listing \u00b7 EstatePro", font=small_font, fill=(255, 255, 255, 200))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return buf


class Command(BaseCommand):
    help = "Seed the database with a demo agent, client, and sample properties."

    def handle(self, *args, **options):
        agent, agent_created = User.objects.get_or_create(
            username="demo_agent",
            defaults={"email": "demo.agent@example.com", "role": "agent"},
        )
        if agent_created:
            agent.set_password("Demo@12345")
            agent.role = "agent"
            agent.save()
            self.stdout.write(self.style.SUCCESS("Created demo agent -> username: demo_agent / password: Demo@12345"))
        else:
            self.stdout.write("Demo agent already exists, reusing it.")

        client, client_created = User.objects.get_or_create(
            username="demo_client",
            defaults={"email": "demo.client@example.com", "role": "client"},
        )
        if client_created:
            client.set_password("Demo@12345")
            client.role = "client"
            client.save()
            self.stdout.write(self.style.SUCCESS("Created demo client -> username: demo_client / password: Demo@12345"))
        else:
            self.stdout.write("Demo client already exists, reusing it.")

        created_count = 0
        first_property = None

        for data in DEMO_PROPERTIES:
            if Property.objects.filter(title=data["title"], agent=agent).exists():
                continue

            prop = Property(
                agent=agent,
                title=data["title"],
                description=data["description"],
                listing_type=data["listing_type"],
                price=data["price"],
                address=data["address"],
                city=data["city"],
                bedrooms=data["bedrooms"],
                bathrooms=data["bathrooms"],
                area_sqft=data["area_sqft"],
                status="available",
            )

            try:
                image_buf = generate_placeholder_image(data["title"], data["color"])
                file_name = data["title"].lower().replace(" ", "_") + ".jpg"
                prop.image.save(file_name, ContentFile(image_buf.read()), save=False)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not generate image for {data['title']}: {e}"))

            prop.save()
            created_count += 1
            if first_property is None:
                first_property = prop

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} new demo properties."))

        # Give the demo client one pending request so the transaction flow has data too
        if first_property and not Transaction.objects.filter(client=client, property=first_property).exists():
            Transaction.objects.create(
                property=first_property,
                client=client,
                transaction_type="buy" if first_property.listing_type == "sale" else "rent",
                amount=first_property.price,
                status="pending",
                message="Hi, I'm interested in this property. Is it still available?",
            )
            first_property.status = "pending"
            first_property.save(update_fields=["status"])
            self.stdout.write(self.style.SUCCESS(f"Created a sample pending request on '{first_property.title}'."))

        self.stdout.write(self.style.SUCCESS(
            "\nDemo data ready.\n"
            "  Agent login:  demo_agent / Demo@12345\n"
            "  Client login: demo_client / Demo@12345\n"
        ))
