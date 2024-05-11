import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrienda_rural.settings")  # Replace with your project settings

import django
django.setup()

from web.models import RegionesChile, Direccion
from django.db.models import Max  # Import Max for finding the next ID

def populate_regiones():
    regiones_data = {
        "Arica y Parinacota": None,
        "Tarapacá": None,
        "Antofagasta": None,
        "Atacama": None,
        "Coquimbo": None,
        "Valparaíso": None,
        "Metropolitana de Santiago": None,
        "Libertador General Bernardo O'Higgins": None,
        "Maule": None,
        "Ñuble": None,
        "Biobío": None,
        "Araucanía": None,
        "Los Ríos": None,
        "Los Lagos": None,
        "Aysén del General Carlos Ibáñez del Campo": None,
        "Magallanes y de la Antártica Chilena": None,
    }

    print("Starting region population...")

    for nombre, _ in regiones_data.items():
        print(f"Processing region: {nombre}") 
        try:
            region, created = RegionesChile.objects.get_or_create(nombre=nombre)
            regiones_data[nombre] = region

            if created:
                print(f"New region created: '{nombre}'")
                # Find the next ID for Direccion based on existing data
                max_id = Direccion.objects.aggregate(Max('id'))['id__max'] or 0
                next_id = max_id + 1

                Direccion.objects.create(calle=nombre, numero=next_id, comuna_id=next_id)  # Create Direccion entry with comuna_id
            else:
                print(f"Region '{nombre}' already exists.")
        except Exception as e:
            print(f"Error processing region '{nombre}': {e}")
    
    print("\nPopulation process complete!")
    print("Existing regions and addresses in database:")
    for region in RegionesChile.objects.all():
        print(region)
        for direccion in region.direccion_set.all():
            print(f"- {direccion}")

populate_regiones()  # Call the function directly
