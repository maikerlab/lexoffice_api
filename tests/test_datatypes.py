import unittest
import uuid
import lexoffice_api.datatypes as dt

class TestAddress(unittest.TestCase):

    def test_address(self):
        contact_id = str(uuid.uuid4())
        address_dict = {
            "contactId": contact_id,
            "name": "Bike & Ride GmbH & Co. KG",
            "supplement": "Gebäude 10",
            "street": "Musterstraße 42",
            "city": "Freiburg",
            "zip": "79112",
            "countryCode": "DE"
        }
        obj = dt.Address(address_dict)
        self.assertEqual(uuid.UUID(contact_id), obj.contact_id)
        self.assertEqual("Bike & Ride GmbH & Co. KG", obj.name)
        self.assertEqual("Gebäude 10", obj.supplement)
        self.assertEqual("Musterstraße 42", obj.street)
        self.assertEqual("Freiburg", obj.city)
        self.assertEqual(79112, obj.zip)
        self.assertEqual("DE", obj.countryCode)

    def test_address_with_invalid_zip(self):
        contact_id = str(uuid.uuid4())
        address_dict = {
            "contactId": contact_id,
            "name": "Bike & Ride GmbH & Co. KG",
            "supplement": "Gebäude 10",
            "street": "Musterstraße 42",
            "city": "Freiburg",
            "zip": "79112a",
            "countryCode": "DE"
        }
        obj = dt.Address(address_dict)
        self.assertEqual(0, obj.zip)

    def test_address_without_supplement(self):
        contact_id = str(uuid.uuid4())
        address_dict = {
            "contactId": contact_id,
            "name": "Bike & Ride GmbH & Co. KG",
            "street": "Musterstraße 42",
            "city": "Freiburg",
            "zip": "79112a",
            "countryCode": "DE"
        }
        obj = dt.Address(address_dict)
        self.assertEqual("", obj.supplement)


class TestLineItem(unittest.TestCase):

    def setUp(self):
        self.line_item = {
            "id": "97b98491-e953-4dc9-97a9-ae437a8052b4",
            "type": "material",
            "name": "Abus Kabelschloss Primo 590",
            "description": "9,5 mm starkes, smoke-mattes Spiralkabel mit integrierter Halterlösung",
            "quantity": 2,
            "unitName": "Stück",
            "unitPrice": {
                "currency": "EUR",
                "netAmount": 13.4,
                "grossAmount": 15.95,
                "taxRatePercentage": 19
            },
            "discountPercentage": 50,
            "lineItemAmount": 13.4
        }

    def test_all_variables_set(self):
        obj = dt.LineItem(self.line_item)
        self.assertEqual(uuid.UUID("97b98491-e953-4dc9-97a9-ae437a8052b4"), obj.id)
        self.assertEqual(dt.Type.MATERIAL, obj.type)
        self.assertEqual("Abus Kabelschloss Primo 590", obj.name)
        self.assertEqual("9,5 mm starkes, smoke-mattes Spiralkabel mit integrierter Halterlösung", obj.description)
        self.assertEqual(2, obj.quantity)
        self.assertEqual("Stück", obj.unit_name)
        self.assertEqual("EUR", obj.unit_price.currency)
        self.assertEqual(13.4, obj.unit_price.net_amount)
        self.assertEqual(15.95, obj.unit_price.gross_amount)
        self.assertEqual(19, obj.unit_price.tax_rate_percentage)
        self.assertEqual(50, obj.discount_percentage)
        self.assertEqual(13.4, obj.line_item_amount)

    def test_type(self):
        self.line_item['type'] = "material"
        obj = dt.LineItem(self.line_item)
        self.assertEqual(dt.Type.MATERIAL, obj.type)
        self.line_item['type'] = "custom"
        obj = dt.LineItem(self.line_item)
        self.assertEqual(dt.Type.CUSTOM, obj.type)
        self.line_item['type'] = "service"
        obj = dt.LineItem(self.line_item)
        self.assertEqual(dt.Type.SERVICE, obj.type)
        self.line_item['type'] = "text"
        obj = dt.LineItem(self.line_item)
        self.assertEqual(dt.Type.TEXT, obj.type)
        # Check invalid type
        self.line_item['type'] = "blabla"
        obj = dt.LineItem(self.line_item)
        self.assertEqual(dt.Type.UNDEFINED, obj.type)

class TestVoucher(unittest.TestCase):

    def test_voucher(self):
        voucher = {
            "id": "57b8d457-1fb6-4ae9-944a-9fe763da2aff",
            "voucherType": "purchaseinvoice",
            "voucherStatus": "open",
            "voucherNumber": "2010096",
            "voucherDate": "2021-06-14T00:00:00.000+02:00",
            "createdDate": "2021-03-22T12:36:22.000+01:00",
            "updatedDate": "2021-03-22T12:36:22.000+01:00",
            "dueDate": "2021-06-21T00:00:00.000+02:00",
            "contactId": "null",
            "contactName": "Sammellieferant",
            "totalAmount": 80.04,
            "openAmount": 80.04,
            "currency": "EUR",
            "archived": False
        }
        obj = dt.Voucher(voucher)
        self.assertEqual(uuid.UUID("57b8d457-1fb6-4ae9-944a-9fe763da2aff"), obj.id)
        self.assertEqual(dt.VoucherStatus.OPEN, obj.voucher_status)
        self.assertEqual(dt.VoucherType.PURCHASE_INVOICE, obj.voucher_type)
        self.assertEqual(None, obj.contact_id)
        self.assertEqual(False, obj.archived)

class TestVoucherList(unittest.TestCase):

    def test_voucherlist(self):
        voucherlist = {
            "content": [
                {
                    "id": "57b8d457-1fb6-4ae9-944a-9fe763da2aff",
                    "voucherType": "purchaseinvoice",
                    "voucherStatus": "open",
                    "voucherNumber": "2010096",
                    "voucherDate": "2021-06-14T00:00:00.000+02:00",
                    "createdDate": "2021-03-22T12:36:22.000+01:00",
                    "updatedDate": "2021-03-22T12:36:22.000+01:00",
                    "dueDate": "2021-06-21T00:00:00.000+02:00",
                    "contactId": "null",
                    "contactName": "Sammellieferant",
                    "totalAmount": 80.04,
                    "openAmount": 80.04,
                    "currency": "EUR",
                    "archived": False
                },
                {
                    "id": "f3d3ae48-30d9-4b56-973a-b3159cbe743c",
                    "voucherType": "invoice",
                    "voucherStatus": "open",
                    "voucherNumber": "RE1012",
                    "voucherDate": "2021-02-14T00:00:00.000+01:00",
                    "createdDate": "2021-03-03T16:52:21.000+01:00",
                    "updatedDate": "2021-03-03T16:52:21.000+01:00",
                    "dueDate": "2021-11-13T00:00:00.000+01:00",
                    "contactId": "777c7793-9fbb-4ec7-9254-0619c199761e",
                    "contactName": "Musterfrau, Erika",
                    "totalAmount": 99.8,
                    "openAmount": 74.8,
                    "currency": "EUR",
                    "archived": False
                },
                {
                    "id": "55aa6de8-d32d-47bd-9c3c-d541ab65a8e8",
                    "voucherType": "invoice",
                    "voucherStatus": "overdue",
                    "voucherNumber": "RE1011",
                    "voucherDate": "2020-10-07T00:00:00.000+02:00",
                    "createdDate": "2020-11-03T16:52:21.000+02:00",
                    "updatedDate": "2020-11-03T16:52:21.000+02:00",
                    "dueDate": "2020-11-06T00:00:00.000+01:00",
                    "contactId": "b08a1ac7-10fc-4214-b875-8491f91479dd",
                    "contactName": "Test GmbH",
                    "totalAmount": 498.8,
                    "openAmount": 498.8,
                    "currency": "EUR",
                    "archived": False
                }
            ],
            "first": True,
            "last": True,
            "totalPages": 1,
            "totalElements": 3,
            "numberOfElements": 3,
            "size": 25,
            "number": 0,
            "sort": [
                {
                    "property": "voucherdate",
                    "direction": "DESC",
                    "ignoreCase": False,
                    "nullHandling": "NATIVE",
                    "ascending": False
                }
            ]
        }
        obj = dt.VoucherList(voucherlist)
        self.assertEqual(3, len(voucherlist['content']))
        self.assertEqual(1, obj.total_pages)
        self.assertEqual(3, obj.total_elements)
        self.assertEqual(3, obj.number_of_elements)
        self.assertEqual(25, obj.size)
        self.assertEqual(0, obj.number)
        self.assertTrue(obj.first)
        self.assertTrue(obj.last)


if __name__ == '__main__':
    unittest.main()
