import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import connection

from store.models import Category, Product

class Command(BaseCommand):
    help = "Popola il database con categorie, prodotti e relazioni many-to-many"

    def handle(self, *args, **options):
        # 1) path alla cartella data (metti i tuoi CSV qui)
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

        # --- Importa le categorie ---
        df_cat = pd.read_csv(os.path.join(base_dir, 'categories.csv'))
        for _, row in df_cat.iterrows():
            Category.objects.update_or_create(
                id=int(row['id']),
                defaults={'name': row['name']}
            )
        self.stdout.write(self.style.SUCCESS("✔️ Categorie importate"))

        # --- Importa i prodotti ---
        df_prod = pd.read_csv(os.path.join(base_dir, 'products.csv'))
        for _, row in df_prod.iterrows():
            Product.objects.update_or_create(
                id=int(row['id']),
                defaults={
                    'name': row['name'],
                    'price': float(row['price']),
                    'stock': int(row['stock']),
                    'available': bool(row['available']),
                    'description': row['description'],
                    'category_id': int(row['category_id']),
                }
            )
        self.stdout.write(self.style.SUCCESS("✔️ Prodotti importati"))

        # --- Popola la many-to-many esterna ---
        df_rel = pd.read_csv(os.path.join(base_dir, 'product_related_categories.csv'))
        with connection.cursor() as cursor:
            for _, row in df_rel.iterrows():
                cursor.execute("""
                    INSERT INTO store_product_related_category (product_id, category_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, [int(row['product_id']), int(row['category_id'])])
        self.stdout.write(self.style.SUCCESS("✔️ Relazioni many-to-many popolate"))