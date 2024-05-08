from .models import Direccion, Usuario, Inmueble

class InvalidTipoUsuarioError(ValueError):
    pass

class InvalidTipoInmuebleError(ValueError):
    pass

class InvalidEstadoInmuebleError(ValueError):
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
    
    def actualizar_usuario(self, rut, Nombre_1, Apellido_1, Nombre_2, Apellido_2, email, telefono,tipo_usuario):
        try:
            usuario = Usuario.objects.get(rut=rut)
            usuario.Nombre_1 = Nombre_1
            usuario.Apellido_1 = Apellido_1
            usuario.Nombre_2 = Nombre_2
            usuario.Apellido_2 = Apellido_2
            usuario.email = email
            usuario.telefono = telefono
            usuario.tipo_usuario = tipo_usuario
            usuario.save()
            print(f"Usuario con rut {rut} actualizado.")
            return {
                'rut': usuario.rut, 
                'nombre': usuario.Nombre_1, 
                'apellido': usuario.Apellido_1, 
                'nombre_2': usuario.Nombre_2, 
                'apellido_2': usuario.Apellido_2, 
                'email': usuario.email, 
                'telefono': usuario.telefono, 
                'tipo_usuario': usuario.tipo_usuario
            }
        except Usuario.DoesNotExist:
            print(f"Usuario con rut {rut} no encontrado.")
            return False
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return False

    def eliminar_usuario(self, rut):
        try:
            usuario = Usuario.objects.get(rut=rut)
            usuario.delete()
            print(f"Usuario con rut {rut} eliminado.")
            return True
        except Usuario.DoesNotExist:
            print(f"Usuario con rut {rut} no encontrado.")
            return False
        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
            return False

    def get_inmueble(self, nombre):
        try:
            inmueble = Inmueble.objects.get(nombre=nombre)
            print(f"Inmueble con nombre {nombre} encontrado.")
            return {
                'nombre': inmueble.nombre,
                'description': inmueble.description,
                'm2_construidos': inmueble.m2_construidos,
                'm2_totales': inmueble.m2_totales,
                'estacionamientos': inmueble.estacionamientos,
                'cantidad_habitaciones': inmueble.cantidad_habitaciones,
                'cantidad_banos': inmueble.cantidad_banos,
                'tipo_de_inmueble': inmueble.tipo_de_inmueble,
                'precio_arriendo': inmueble.precio,
                'estado': inmueble.estado
            }
        except Inmueble.DoesNotExist:
            print(f"Inmueble con nombre {nombre} no encontrado.")
            return False
        except Exception as e:
            print(f"Error al consultar el inmueble: {e}")
            return False
        
    def agregar_inmueble(self, nombre, description, m2_construidos, m2_totales, estacionamientos, cantidad_habitaciones, cantidad_banos, tipo_de_inmueble, precio, estado):
        try:
            tipo_de_inmueble_opcion = tipo_de_inmueble.lower()
            if tipo_de_inmueble_opcion in Inmueble.TIPO_DE_INMUEBLE:
                tipo_de_inmueble = tipo_de_inmueble_opcion
            else:
                print(f"Las opciones válidas son: {Inmueble.TIPO_DE_INMUEBLE}")
                raise InvalidTipoInmuebleError(f"Opción inválida: '{tipo_de_inmueble_opcion}'.")
        except Exception as e:
            print(f"Error al agregar el inmueble: {e}")
            return False
        

        