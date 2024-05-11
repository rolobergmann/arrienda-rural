import django
django.setup()  # Set up Django environment (if running outside of `manage.py shell`)

from django.db.models import Prefetch
from web.models import Inmueble, RegionesChile, ComunasChile

def generate_inmueble_list_by_region():
    """Generates a text file with inmuebles grouped by region (ordered)."""
    with open("inmuebles_por_region.txt", "w", encoding="utf-8") as f:
        # Fetch all regions in alphabetical order
        regions = RegionesChile.objects.order_by('nombre')

        for region in regions:
            # Filter inmuebles for the current region (including all communes within the region)
            inmuebles = Inmueble.objects.filter(
                estado=True, 
                direccion__comuna__region=region
            ).prefetch_related(
                Prefetch("direccion__comuna", queryset=ComunasChile.objects.only("nombre"))
            )

            if inmuebles.exists():  # Only write if there are inmuebles in the region
                f.write(f"\n**{region.nombre}**\n\n")  # Region header

                for inmueble in inmuebles:
                    f.write(f"- {inmueble.nombre}: {inmueble.description} ({inmueble.direccion.comuna.nombre})\n")

# Run the function to generate the file
generate_inmueble_list_by_region()
