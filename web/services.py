from .models import Direccion, Usuario, Inmueble

class InvalidTipoUsuarioError(ValueError):
    pass
class Services:

    def get_usuario(self, rut):
        try: 
            usuario = Usuario.objects.get(rut=rut)  # Retrieve the Usuario
            print(f"Usuario con rut {rut} encontrado.")
            return {
                'rut': usuario.rut, 
                'nombre': usuario.Nombre_1, 
                'apellido': usuario.Apellido_1
            }
        except Usuario.DoesNotExist:
            print(f"Usuario con rut {rut} no encontrado." )
            return False
        except Exception as e:
            print(f"Error al consultar el usuario: {e}")  # More precise error handling
            return False

    def agregar_usuario(self, rut, Nombre_1, Apellido_1, Nombre_2, Apellido_2, email, telefono,tipo_usuario):
        try:
            tipo_usuario_opcion = tipo_usuario.lower()
            if tipo_usuario_opcion in Usuario.TIPO_USUARIO_ELECCIONES:
                tipo_usuario = tipo_usuario_opcion
            else:
                print(f"Las opciones válidas son: {Usuario.TIPO_USUARIO_ELECCIONES}")
                raise InvalidTipoUsuarioError(f"Opción inválida: '{tipo_usuario_opcion}'.") 
            usuario = Usuario.objects.create(rut=rut, Nombre_1=Nombre_1, Apellido_1=Apellido_1, Nombre_2=Nombre_2, Apellido_2=Apellido_2, email=email, telefono=telefono,tipo_usuario=tipo_usuario)
            print(f"Usuario con rut {rut} agregado.")
            return {
                'rut': usuario.rut, 
                'nombre': usuario.Nombre_1, 
                'apellido': usuario.Apellido_1
            }
        except Exception as e:
            print(f"Error al agregar el usuario: {e}")
            return False