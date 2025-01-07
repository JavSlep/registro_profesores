from django.test import TestCase
from .models import *

class CdpModelTests(TestCase):

    def setUp(self):
        # Crear instancias necesarias para las pruebas
        subtitulo = Subtitulo.objects.create(
            id="1",
            n_subtitulo="01",
            denominacion="Subtitulo 1"
        )
        self.subtitulo_presupuestario = SubtituloPresupuestario.objects.create(
            id="1",
            subtitulo=subtitulo,
            ley_presupuestaria_subtitulo=1000
        )
        item = Item.objects.create(
            id="1",
            subtitulo=subtitulo,
            n_item="01",
            denominacion="Item 1"
        )
        item2 = Item.objects.create(
            id="2",
            subtitulo=subtitulo,
            n_item="02",
            denominacion="Item 2"
        )
        self.item_presupuestario = ItemPresupuestario.objects.create(
            id="1",
            subtitulo_presupuestario=self.subtitulo_presupuestario,
            item=item,
            ley_presupuestaria_item=0,
            monto_comprometido=200
        )
        self.item_presupuestario2 = ItemPresupuestario.objects.create(
            id="2",
            subtitulo_presupuestario=self.subtitulo_presupuestario,
            item=item2,
            ley_presupuestaria_item=0,
            monto_comprometido=200
        )
        self.cdp = Cdp.objects.create(
            id="1",
            establecimiento=None,
            unidad=None,
            ItemPresupuestario=self.item_presupuestario,
            numero_requerimiento=1,
            fondo="SEP",
            cdp="CDP-1",
            folio_sigfe="12345",
            documento="Doc1",
            monto=300, #Monto que se suma al item
            detalle="Detalle 1",
            otros="Otros 1",
            fecha_cdp="2024-12-30",
            fecha_guia_requerimiento="2024-12-30"
        )
        self.cdp2 = Cdp.objects.create(
            id="2",
            establecimiento=None,
            unidad=None,
            ItemPresupuestario=self.item_presupuestario,
            numero_requerimiento=1,
            fondo="SEP",
            cdp="CDP-2",
            folio_sigfe="12346",
            documento="Doc2",
            monto=100,#Monto que se suma al item
            detalle="Detalle 2",
            otros="Otros 2",
            fecha_cdp="2024-12-30",
            fecha_guia_requerimiento="2024-12-30"
        )

    def test_saldo_comprometido(self): #Esto es por itemPresupuestario
        # Probar el método saldo_comprometido
        print(f"Saldo comprometido: {self.item_presupuestario.saldo_comprometido} en la partida {self.item_presupuestario.item.denominacion}")
        self.assertEqual(self.item_presupuestario.saldo_comprometido, 600)

    def test_saldo_comprometido2(self): #Esto es por itemPresupuestario
        # Probar el método saldo_comprometido en la segunda partida
        print(f"Saldo comprometido: {self.item_presupuestario2.saldo_comprometido} en la partida {self.item_presupuestario2.item.denominacion}")
        self.assertEqual(self.item_presupuestario2.saldo_comprometido, 200)

    def test_monto_por_comprometer(self): # Esto es por SubtituloPresupuestario
        # Probar el método monto_por_comprometer
        print(f"Monto por comprometer: {self.subtitulo_presupuestario.monto_por_comprometer}")
        self.assertEqual(self.subtitulo_presupuestario.monto_por_comprometer, 200)
    