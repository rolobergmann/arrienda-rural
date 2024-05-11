from django.db.models import Prefetch
from web.models import Inmueble, ComunasChile

def generate_inmueble_list():
    """Generates a text file with inmuebles grouped by comuna."""
    with open("inmuebles_por_comuna.txt", "w", encoding="utf-8") as f:
        # Efficiently prefetch related comuna data
        inmuebles = Inmueble.objects.prefetch_related(
            Prefetch("direccion__comuna", queryset=ComunasChile.objects.only("nombre"))
        )

        current_comuna = None
        for inmueble in inmuebles:
            comuna = inmueble.direccion.comuna
            if comuna != current_comuna:
                current_comuna = comuna
                f.write(f"\n**{comuna.nombre}**\n\n")  # Comuna header

            f.write(f"- {inmueble.nombre}: {inmueble.description}\n")

# Run the function to generate the file
generate_inmueble_list()