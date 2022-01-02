import datetime
import os
import unittest
import uuid

from requests.exceptions import RequestException
from lexoffice_api import api
from dotenv import load_dotenv

from lexoffice_api.datatypes import VoucherType, VoucherStatus

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
        voucher_list = self.client.get_voucherlist(voucher_type=VoucherType.INVOICE, status=statuses, size=50)
        self.assertEqual(len(voucher_list.content), 50)
        valid_statuses = [VoucherStatus.PAID, VoucherStatus.OPEN, VoucherStatus.DRAFT, VoucherStatus.OVERDUE]
        for voucher in voucher_list.content:
            self.assertTrue(voucher.voucher_status in valid_statuses, msg=f'{voucher.voucher_status.value} is not a valid status')

    def test_get_invoice(self):
        self.assertRaises(RequestException, self.client.get_invoice, 'invalid-uuid')
        invoice_id = 'ba41840a-cab7-40fc-97d2-60a10a2d57e3'
        invoice = self.client.get_invoice(uuid.UUID(invoice_id))
        self.assertEqual(invoice.id, uuid.UUID(invoice_id))
        self.assertIsNotNone(invoice.line_items)


if __name__ == '__main__':
    unittest.main()
