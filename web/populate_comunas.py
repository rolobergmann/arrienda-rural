import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrienda_rural.settings")

import django
django.setup()

from web.models import ComunasChile, RegionesChile

def populate_comunas():
    comunas_data = {

"Valparai­so": {
    "Valparaiso": None,
    "Casablanca": None,
    "Concón": None,
    "Juan Fernández": None,
    "Puchuncaví": None,
    "Quintero": None,
    "Viña del Mar": None,
    "Isla de Pascua": None,
    "Los Andes": None,
    "Calle Larga": None,
    "Rinconada": None,
    "San Esteban": None,
    "La Ligua": None,
    "Cabildo": None,
    "Papudo": None,
    "Petorca": None,
    "Zapallar": None,
    "Quillota": None,
    "La Cruz": None,
    "Nogales": None,
    "Hijuelas": None,
    "Olmué": None,
    "Limache": None,
    "San Antonio": None,
    "Algarrobo": None,
    "Cartagena": None,
    "El Quisco": None,
    "El Tabo": None,
    "Santo Domingo": None,
    "San Felipe": None,
    "Catemu": None,
    "Llaillay": None,
    "Panquehue": None,
    "Putaendo": None,
    "Santa María": None,
    },
}
    for region_name, comunas in comunas_data.items():
        try:
            region = RegionesChile.objects.get(nombre=region_name)
        except RegionesChile.DoesNotExist:
            print(f"Error: Region '{region_name}' not found.")
            continue
            
        for comuna_name in comunas:
            try:
                comuna, created = ComunasChile.objects.get_or_create(nombre=comuna_name, region=region)
                if created:
                    print(f"New commune created: '{comuna_name}' (Region: {region_name})")
            except Exception as e:  
                print(f"Error processing commune '{comuna_name}' (Region: {region_name}): {e}")

    print("\nPopulation process complete!")
    print("Existing regions and communes in database:")
    for region in RegionesChile.objects.all():
        print(region)
        for comuna in region.comunaschile_set.all():
            print(f"- {comuna}")

# ... (remove the import of 'populate_regiones') ...

# Call the function directly (without the if __name__ == '__main__' block)
populate_comunas()