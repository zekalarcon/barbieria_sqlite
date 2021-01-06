import sqlite3
from datetime import date


def agregar_operacion(cursor, fecha):

    peluqueria_operacion = input("Ingrese operacion\n> ").upper()
    nombre_cliente = input("Ingrese nombre cliente\n> ").upper()
    telefono_cliente = input("Ingrese telefono cliente\n> ")
    precio = input("Ingrese precio\n> ")

    cursor.execute("INSERT INTO operaciones VALUES (null, '{}', '{}', '{}', '{}', '{}')".format(
        fecha, peluqueria_operacion, nombre_cliente, telefono_cliente, precio))

    trabajo = cursor.lastrowid

    while True:
        agregar_producto = input(
            'Desea agregar algun producto (SI o NO)?\n>').upper()
        if agregar_producto == 'SI':
            producto = input('Ingrese producto a utilizar:\n>').upper()
            cantidad = input('Ingrese cantidad:\n>')
            accion = 'EGRESO'

            cursor.execute("INSERT INTO stock VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                fecha, producto, cantidad, accion, trabajo))
        else:
            break


def stock(cursor, fecha):

    opcion = input(
        "\nIntroduce una opción:"
        "\n[1] Agregar stock"
        "\n[2] Stock productos"
        "\nCualquier tecla para volver atras\n\n> ")

    if opcion == '1':

        while True:
            producto_stock = input(
                'Ingrese producto a stockear o ENTER para salir:\n>').upper()
            if producto_stock == '':
                break
            cantidad_stock = input('Ingrese cantidad:\n>')
            accion = 'INGRESO'
            trabajo = None

            cursor.execute("INSERT INTO stock VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                fecha, producto_stock, cantidad_stock, accion, trabajo))

    elif opcion == '2':

        while True:

            egreso = []
            ingreso = []

            producto = input(
                'Ingrese producto para saber stock o ENTER para salir:\n>').upper()

            if producto == '':
                break

            cursor.execute(
                "SELECT * FROM stock WHERE PRODUCTO_STOCK = '%s' and ACCION = 'INGRESO'" % (producto))
            row = cursor.fetchall()

            for i in row:
                ingreso.append(i[2])

            cursor.execute(
                "SELECT * FROM stock WHERE PRODUCTO_STOCK = '%s' and ACCION = 'EGRESO'" % (producto))
            row = cursor.fetchall()

            for i in row:
                egreso.append(i[2])

            stock = sum(ingreso) - sum(egreso)
            print(f'{producto}: {stock} grs.')


def historial(cursor):

    cliente = input('Ingrese nombre cliente:\n>').upper()

    cursor.execute(
        "SELECT * FROM operaciones JOIN stock WHERE NOMBRE_CLIENTE='%s' and operaciones.ID = stock.TRABAJO_ID" % (cliente))
    row = cursor.fetchall()

    for i in row:
        print(
            f'{i[1]} Trabajo realizado: {i[2]} Producto: {i[7]} Cantidad: {i[8]} grs.')


def total(cursor, fecha):

    suma = []

    opcion = input(
        "\nIntroduce una opción:"
        "\n[1] Total dia"
        "\n[2] Total rango fechas"
        "\nCualquier tecla para volver atras\n\n> ")

    if opcion == '1':

        cursor.execute(
            "SELECT * FROM operaciones WHERE FECHA = '%s' " % (fecha))
        row = cursor.fetchall()

        for i in row:
            suma.append(i[5])

        print(f'El total del dia es: ${sum(suma)}')

    elif opcion == '2':

        inicio = input('Ingrese primer fecha (EJ: 2021-01-25):\n>')
        fin = input('Ingrese sugunda fecha (EJ: 2021-01-25):\n>')

        cursor.execute(
            "SELECT * FROM operaciones WHERE FECHA >= '%s' and FECHA <= '%s' " % (inicio, fin))
        row = cursor.fetchall()

        for i in row:
            suma.append(i[5])

        print(f'El total entre las fechas seleccionadas es: ${sum(suma)}')


def main():

    while True:
        conexion = sqlite3.connect('operacion peluqueria.db')
        cursor = conexion.cursor()
        fecha = date.today()

        print("\nBienvenido a la barbieria!")

        opcion = input(
            "\nIntroduce una opción:"
            "\n[1] Agregar operacion"
            "\n[2] Agregar stock / Stock productos"
            "\n[3] Historial cliente"
            "\n[4] Total $ dia o entre fechas"
            "\n[5] Salir del programa\n\n> ")

        if opcion == "1":
            agregar_operacion(cursor, fecha)

        elif opcion == '2':
            stock(cursor, fecha)

        elif opcion == '3':
            historial(cursor)

        elif opcion == '4':
            total(cursor, fecha)

        elif opcion == "5":
            print("Hasta la proxima!")
            break

        else:
            print("Opción incorrecta")

        conexion.commit()
        conexion.close()


if __name__ == "__main__":
    main()
