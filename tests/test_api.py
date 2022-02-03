import os
import unittest
import uuid

from requests.exceptions import RequestException
from src.lexoffice import api
from src.lexoffice.datatypes import VoucherType, VoucherStatus

from dotenv import load_dotenv

from src.lexoffice.exceptions import LexofficeException

load_dotenv()

class TestLexOfficeApi(unittest.TestCase):

    def setUp(self):
        self.client = api.LexofficeClient(os.environ.get('API_KEY'))

    def test_ping(self):
        self.assertTrue(self.client.ping())

    def test_get_voucherlist(self):
        statuses = []
        self.assertRaises(ValueError, self.client.get_voucherlist, voucher_type=VoucherType.INVOICE, status=statuses, size=50)
        statuses = [VoucherStatus.PAID, VoucherStatus.OPEN, VoucherStatus.DRAFT]
        voucher_list = self.client.get_voucherlist(voucher_type=VoucherType.INVOICE, status=statuses, size=250)
        self.assertEqual(len(voucher_list.content), 250)
        self.assertEqual(voucher_list.number_of_elements, 250)
        self.assertTrue(voucher_list.first)
        if voucher_list.total_elements > 250:
            self.assertFalse(voucher_list.last)
        else:
            self.assertTrue(voucher_list.last)
        self.assertEqual(1, voucher_list.number)
        valid_statuses = [VoucherStatus.PAID, VoucherStatus.OPEN, VoucherStatus.DRAFT, VoucherStatus.OVERDUE]
        for voucher in voucher_list.content:
            self.assertTrue(voucher.voucher_status in valid_statuses, msg=f'{voucher.voucher_status.value} is not a valid status')

    def test_get_invoice(self):
        self.assertRaises(RequestException, self.client.get_invoice, 'invalid-uuid')
        invoice_id = 'ba41840a-cab7-40fc-97d2-60a10a2d57e3'
        invoice = self.client.get_invoice(uuid.UUID(invoice_id))
        self.assertEqual(invoice.id, uuid.UUID(invoice_id))
        self.assertIsNotNone(invoice.line_items)

    def test_different_invoices(self):
        statuses = [VoucherStatus.PAID, VoucherStatus.OPEN, VoucherStatus.DRAFT]
        voucher_list = self.client.get_voucherlist(voucher_type=VoucherType.INVOICE, status=statuses, size=10)
        for voucher in voucher_list.content:
            try:
                invoice = self.client.get_invoice(voucher.id)
                self.assertIsNotNone(invoice.id)
            except LexofficeException as ex:
                print(ex.msg)
                pass


if __name__ == '__main__':
    unittest.main()
