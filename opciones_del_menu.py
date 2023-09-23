import os
import datetime
import time
from rich import print
from rich.table import Table
from email_validator import validate_email, EmailNotValidError

def comprobar_servicio(detalles_totales):
    while True:
        if not detalles_totales:
            servicio = input('\nServicio a realizar: ')
            if servicio.strip():
                return servicio
            else:
                print('Tiene que introducir al menos un servicio')

        else:
            print('\n[#9999FF](Dejar vacío para terminar)[#/9999FF]')
            servicio = input('Servicio a realizar: ')
            return servicio

def comprobar_precio(servicio):
    while True:
        try:
            while True:
                precio_del_servicio = float(input(f'Precio del servicio {servicio}: '))
                if precio_del_servicio > 0 and (precio_del_servicio*100)%1 == 0:
                    break
                else:
                    print('El precio tiene que ser mayor a 0 y no puede tener más de 2 decimales\n')
        except ValueError:
            print('Ese no es un número válido. Intenta de nuevo\n')
        except Exception as ex:
            print(f'Ocurrió el error: {ex}. Intente de nuevo\n')
        else:
            break

    return precio_del_servicio

def comprobar_fecha():
    fecha_actual = datetime.date.today()
    print('[#9999FF](No posterior a la fecha actual)[/#9999FF]')
    while True:
        try:
            while True:
                fecha_proporcionada = input('Fecha de la nota (dd/mm/aaaa): ')
                fecha_de_nota = datetime.datetime.strptime(fecha_proporcionada,"%d/%m/%Y").date()
                if fecha_de_nota <= fecha_actual:
                        break
                else:
                    print('La fecha no puede ser posterior a la actual del sistema\n')
        except ValueError:
            print('Tipo de formato no válido. Intente de nuevo\n')
        except Exception as error:
            print(f'Ocurrió un problema: {error}\n')
        else:
            break

    return fecha_de_nota

def comprobar_nombre():
    while True:
        nombre_del_cliente = input('\nNombre del cliente: ')
        if nombre_del_cliente:
            break
        else:
            print('El nombre del cliente no debe quedar vacío. Intente de nuevo')

    return nombre_del_cliente

def comprobar_RFC():
    RFC = input('\nRFC del Cliente: ')
    
    if len(RFC) == 12:
        if not RFC[:3].isalpha():
            print(f'Los primeros 3 caracteres del RFC deben ser letras para personas morales')
            return False
        else:
            digitos_fecha = [RFC[digito:digito+2] for digito in range(3,9,2)]
        
        

    elif len(RFC) == 13:
        if not (RFC[:4].isalpha() and RFC[1].upper() in ('AEIOU')):
            print(f'Los primeros 4 caracteres del RFC deben ser letras y el segundo una vocal para personas físicas')
            return False
        else:
            digitos_fecha = [RFC[digito:digito+2] for digito in range(4,10,2)]
        
    else:
        print('La longitud del RFC debe ser de 13 caracteres para personas físicas o 12 para personas morales')
        return False
    
    fecha = '/'.join(digitos_fecha)

    try:
        fecha_correcta = datetime.datetime.strptime(fecha,"%y/%m/%d").date()
        return RFC
    
    except ValueError:
        print('Fecha en RFC no válida')
        return False

    except Exception as exc:
        print(f'Ocurrió un error: {exc}')
        return False

def comprobar_correo():
    while True:
        correo = input('\nCorreo electrónico del cliente: ')
        try:
            v = validate_email(correo)
            return correo
        
        except EmailNotValidError as e:
            print(f'Ocurrió un problema: {e}')
        
        except Exception as e:
            print(f'Ocurrió un problema: {e}')

class RegistrarNota:
    def __init__(self, folio):

        os.system('cls')

        self.informacion_de_nota()
        self.detalles_de_nota()
        self.detalles_de_nota_a_str()
        self.retornar_datos()
        self.mostrar_nota(folio)

    def informacion_de_nota(self):
        os.system('cls')
        print('[#7AFFFF]--Información de la Nota--[#/7AFFFF]\n')

        self.fecha_de_nota = comprobar_fecha()
        self.nombre_del_cliente = comprobar_nombre()

        while True:
            self.RFC_del_cliente = comprobar_RFC()
            if self.RFC_del_cliente:
                break

        self.correo_del_cliente= comprobar_correo()


    def detalles_de_nota(self):
        os.system('cls')
        print('[#7AFFFF]--Detalles de la Nota--[#/7AFFFF]\n')

        self.monto_total = 0
        self.detalles = {}

        while True:  
            servicio = comprobar_servicio(self.detalles)
            if not servicio:
                break
                
            print('\n[#9999FF](En número entero o con decimales. Mayor a cero)[#/9999FF]')
            precio_del_servicio = comprobar_precio(servicio)

            self.detalles[servicio] = precio_del_servicio
            self.monto_total += precio_del_servicio
        

    def detalles_de_nota_a_str(self):
        self.detallesNota = '[#9999FF]|[/#9999FF] '
        for servicio, precio in self.detalles.items():
            self.detallesNota += f'{servicio}: {precio} [#9999FF]|[/#9999FF] '


    def retornar_datos(self):

        datos_recolectados = (self.fecha_de_nota, self.nombre_del_cliente, self.RFC_del_cliente, self.correo_del_cliente, self.monto_total, self.detallesNota)

        return datos_recolectados

    def mostrar_nota(self, folio):
        os.system('cls')
        nota = Table(title='[#7AFFFF]--Nueva nota registrada--[/#7AFFFF]', )
    
        nota.add_column("Detalles", justify="left", style="#9999FF")
        nota.add_column("Datos", justify="left", style="white")

        nota.add_row('Folio', f'{folio}')
        nota.add_row('Fecha', f'{self.fecha_de_nota}')
        nota.add_row('Nombre del cliente', f'{self.nombre_del_cliente}')
        nota.add_row('RFC', f'{self.RFC_del_cliente.upper()}')
        nota.add_row('Correo', f'{self.correo_del_cliente}')
        nota.add_row('Monto a pagar', f'{self.monto_total}')
        nota.add_row('Detalle de nota', f'{self.detallesNota}')
        print(nota, '\n')
    
    def aceptacion_de_nota(self, folios):
        while True:
            aceptar = input('| s - Sí | n - No |\n\n')
            print()
            if aceptar.upper() in ('S', 'SI', 'SÍ'):
                for i in range(3):
                    time.sleep(.3)
                    print('[green].[/green]', end='  ')
                print('[green]Registro completado[/green]')
                time.sleep(.8)
                return True
            
            elif aceptar.upper() in ('N', 'NO'):
                for i in range(3):
                    time.sleep(.3)
                    print('[red].[/red]', end='  ')
                print('[red]Registro cancelado[/red]')
                time.sleep(.8)
                return False
            else:
                print('Opción no válida. Intente de nuevo')

class ConsultasYReportes:

    def __init__(self, notas_registradas):
        self.notas_registradas = notas_registradas
        
        while True:
            os.system('cls')
            self.menu_consultas_y_reportes()

            match self.eleccion_consulta:
                case 1:
                    self.consulta_por_periodo()
                case 2:
                    self.consulta_por_folio()
                case 3:
                    break

    def menu_consultas_y_reportes(self):
        print('''
[#9999FF]CONSULTAS Y REPORTES[/#9999FF]
              
[#7AFFFF]--Menú Consultas--[/#7AFFFF]

1 - Consulta por período
2 - Consulta por folio
3 - Regresar al menú principal
              
''')
        while True:
            try:
                self.eleccion_consulta = int(input('Elija una opción (indicando su respectivo número): '))
            except ValueError:
                print('Opción no válida. Intente de nuevo')
            else:
                if self.eleccion_consulta > 0 and self.eleccion_consulta <= 3:
                    break
                else:
                    print('Opción no válida. Intente de nuevo')
        
                    
    def consulta_por_periodo(self):

        os.system('cls')

        print('[#7AFFFF]--Consulta por periodo--[#/7AFFFF]\n')
        
        while True:
            try:
                self.respuesta = input('Ingrese su fecha inicial (dd/mm/aaaa): ')
                self.fecha_inicial = datetime.datetime.strptime(self.respuesta,"%d/%m/%Y").date()
        
                self.respuesta = input('Ingrese su fecha final (dd/mm/aaaa): ')
                self.fecha_final = datetime.datetime.strptime(self.respuesta,"%d/%m/%Y").date()
            except ValueError:
                print('Tipo de formato no válido. Intente de nuevo\n')
            except Exception as error:
                print(f'Ocurrió un problema: {error}\n')
            else:
                break

        notas_del_periodo = Table(title="\n[#7AFFFF]--Notas dentro del perído--[/#7AFFFF]")
        notas_del_periodo.add_column("Folio", justify="left", style="#9999FF")
        notas_del_periodo.add_column("Datos de la nota", justify="left", style="white")

        contador = 0
        for folio, datos in self.notas_registradas.items():
            fecha = datos[0]
            if fecha >= self.fecha_inicial and fecha <= self.fecha_final:
                notas_del_periodo.add_row(f'{folio}', f'{fecha}, {datos[1]}, {datos[2]}, {datos[3]}, {datos[4]}')
                contador += 1
                
        if contador == 0:
            print('\n[red]No existen notas dentro de este período[/red]\n')
        else:
            print(notas_del_periodo)
        input('Presione Enter para continuar\n')
    
    def consulta_por_folio(self):

        os.system('cls')

        print('[#7AFFFF]--Consulta por folio--[#/7AFFFF]\n')

        print('\n[#9999FF](En número entero)[#/9999FF]')
        
        

        while True:
            try:
                folio_consutado = int(input('Folio a Consultar: '))
            except ValueError:
                print('Ese no es un número válido.\n')
            except Exception as error:
                print('Ocurrió un problema. Intente de nuevo')
            else:
                if folio_consutado in self.notas_registradas.keys():
                    break
                else:
                    print("La nota no se encuentra en el sistema o corresponde a una nota cancelada, vuelve a intentarlo\n")
                    input('Presione Enter para continuar')
                    return True

        datos_consultados = self.notas_registradas[folio_consutado]

        os.system('cls')
        
        nota_consultada = Table(title=f'[#7AFFFF]--Nota consultada--[/#7AFFFF]')

        nota_consultada.add_column("Detalles", justify="left", style="#9999FF")
        nota_consultada.add_column("Datos", justify="left", style="white")

        nota_consultada.add_row('Folio', f'{folio_consutado}')
        nota_consultada.add_row('Fecha', f'{datos_consultados[0]}')
        nota_consultada.add_row('Nombre del cliente', f'{datos_consultados[1]}')
        nota_consultada.add_row('RFC', f'{datos_consultados[2].upper()}')
        nota_consultada.add_row('Correo', f'{datos_consultados[3]}')
        nota_consultada.add_row('Monto a pagar', f'{datos_consultados[4]}')
        nota_consultada.add_row('Detalle de nota', f'{datos_consultados[5]}')

        print(nota_consultada)

        input('Presione Enter para continuar\n')

class CancelarNota:
    def __init__(self, notas_registradas, notas_canceladas):
        self.notas_registradas = notas_registradas
        self.notas_canceladas = notas_canceladas
        self.ProcesoCancelacion()

    def ProcesoCancelacion(self):

            while True:
                try:
                    FolioACancelar = int(input("\nIngresa el folio de la nota que deseas cancelar: "))
                except ValueError:
                    print('Ingrese sólo números enteros')
                except Exception as error:
                    print(f'Ocurrió un problema {error}')
                else:
                    if FolioACancelar in self.notas_registradas.keys():
                        break
                    else:
                        print("La nota no se encuentra en el sistema o corresponde a una nota ya cancelada, vuelve a intentarlo\n")
                        input('Presione Enter para continuar')
                        return True

            datos_de_la_nota = self.notas_registradas[FolioACancelar]

            os.system('cls')
            nota_a_cancelar = Table(title='[#7AFFFF]--Nota a Cancelar--[/#7AFFFF]')

            nota_a_cancelar.add_column("Detalles", justify="left", style="#9999FF")
            nota_a_cancelar.add_column("Datos", justify="left", style="white")

            nota_a_cancelar.add_row('Folio', f'{FolioACancelar}')
            nota_a_cancelar.add_row('Fecha', f'{datos_de_la_nota[0]}')
            nota_a_cancelar.add_row('Nombre del cliente', f'{datos_de_la_nota[1]}')
            nota_a_cancelar.add_row('RFC', f'{datos_de_la_nota[2]}')
            nota_a_cancelar.add_row('Correo', f'{datos_de_la_nota[3]}')
            nota_a_cancelar.add_row('Monto a pagar', f'{datos_de_la_nota[4]}')
            nota_a_cancelar.add_row('Detalle de nota', f'{datos_de_la_nota[5]}')

            print(nota_a_cancelar, '\n')

            while True:
                aceptar = input("¿Quiere cancelar definitivamente la nota?\n| s - Sí | n - No |\n")

                if aceptar.upper() in ('S','SI', 'SÍ'):
                    self.notas_canceladas[FolioACancelar] = self.notas_registradas[FolioACancelar]

                    del self.notas_registradas[FolioACancelar]
                    print("[green]Su nota ha sido cancelada[/green]")
                    input('Presione Enter para continuar\n')
                    break

                elif aceptar.upper() in ('N', 'NO'):
                    print("[red]La nota no fue cancelada[/red]")
                    input('Presione Enter para continuar\n')
                    break

                else:
                    print('Opción no válida. Intente de nuevo')

class RecuperarNota:
    def __init__(self, notas_canceladas, notas_registradas) -> None:
        self.notas_canceladas = notas_canceladas
        self.notas_registradas = notas_registradas

        if self.notas_canceladas:
            self.mostrar_notas_canceladas()
            if self.preguntar_recuperación():
                self.recuperar_nota()
        else:
            print('[red]No hay notas canceladas en el sistema[/red]\n')
            input('Presione Enter para continuar\n')

    def mostrar_notas_canceladas(self):
        t_notas_canceladas = Table(title='[#7AFFFF]--Notas actualmente canceladas--[/#7AFFFF]')

        t_notas_canceladas.add_column('Folio', style='#9999FF')
        t_notas_canceladas.add_column('Datos de la nota', style='white')

        for folio, datos in self.notas_canceladas.items():
            t_notas_canceladas.add_row(f'{folio}', f'{datos[0]}, {datos[1]}, {datos[2]}, {datos[3]}, {datos[4]}')

        print(t_notas_canceladas)

    def preguntar_recuperación(self):

        while True:
            recuperar = input("¿Quiere recuperar alguna nota?\n| s - Sí | n - No |\n")

            if recuperar.upper() in ('S', 'SI', 'SÍ'):
                return True

            elif recuperar.upper() in ('N', 'NO'):
                print("[red]ninguna nota fue recuperada[/red]")
                input('Presione Enter para continuar\n')
                return False

            else:
                print('Opción no válida. Intente de nuevo\n')

    def recuperar_nota(self):
        while True:
            try:
                folio_a_recuperar = int(input('\nIngrese el folio de la nota que quiere recuperar: '))
            except ValueError:
                print('Ingrese sólo números enteros\n')
            except Exception as error:
                print(f'Ocurrió un problema: {error}\n')
            else:
                if folio_a_recuperar in self.notas_canceladas.keys():
                    break
                else:
                    print("el folio no corresponde a una nota cancelada. Intente de nuevo\n")
                    input('Presione Enter para continuar')
                    return True
        
        os.system('cls')

        datos_recuperacion = self.notas_canceladas[folio_a_recuperar]

        nota_recuperar = Table(title='[#7AFFFF]--Nota a recuperar--[/#7AFFFF]', )
    
        nota_recuperar.add_column("Detalles", justify="left", style="#9999FF")
        nota_recuperar.add_column("Datos", justify="left", style="white")

        nota_recuperar.add_row('Folio', f'{folio_a_recuperar}')
        nota_recuperar.add_row('Fecha', f'{datos_recuperacion[0]}')
        nota_recuperar.add_row('Nombre del cliente', f'{datos_recuperacion[1]}')
        nota_recuperar.add_row('RFC', f'{datos_recuperacion[2]}')
        nota_recuperar.add_row('Correo', f'{datos_recuperacion[3]}')
        nota_recuperar.add_row('Monto a pagar', f'{datos_recuperacion[4]}')
        nota_recuperar.add_row('Detalle de nota', f'{datos_recuperacion[5]}')

        print(nota_recuperar)

        while True:
            confirmacion_recuperar = input("\n¿Quiere recuperar esta nota?\n| s - Sí | n - No |\n")

            if confirmacion_recuperar.upper() in ('S', 'SI', 'SÍ'):

                self.notas_registradas[folio_a_recuperar] = self.notas_canceladas[folio_a_recuperar]
                del self.notas_canceladas[folio_a_recuperar]
                print("[green]Su nota ha sido recuperada[/green]")
                input('Presione Enter para continuar\n')
                break

            elif confirmacion_recuperar.upper() in ('N', 'NO'):
                print("[red]La nota no fue recuperada[/red]")
                input('Presione Enter para continuar\n')
                break

            else:
                print('Opción no válida. Intente de nuevo\n')
