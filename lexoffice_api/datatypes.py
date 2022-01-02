import enum
from datetime import datetime
import uuid

class VoucherType(enum.Enum):
    SALES_INVOICE = "salesinvoice"
    SALES_CREDIT_NOTE = "salescreditnote"
    PURCHASE_INVOICE = "purchaseinvoice"
    PURCHASE_CREDIT_NOTE = "purchasecreditnote"
    INVOICE = "invoice"
    DOWN_PAYMENT_INVOICE = "downpaymentinvoice"
    CREDIT_NOTE = "creditnote"
    ORDER_CONFIRMATION = "orderconfirmation"
    QUOTATION = "quotation"
    DELIVERY_NOTE = "deliverynote"

class VoucherStatus(enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    PAIDOFF = "paidoff"
    VOIDED = "voided"
    TRANSFERRED = "transferred"
    SEPADEBIT = "sepadebit"
    OVERDUE = "overdue"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Type(enum.Enum):
    SERVICE = "service"
    MATERIAL = "material"
    CUSTOM = "custom"
    TEXT = "text"
    UNDEFINED = "undefined"

class Address:
    contact_id: uuid.uuid4
    name: str
    supplement: str
    street: str
    city: str
    zip: int
    countryCode: str

    def __init__(self, address: dict):
        self.contact_id = uuid.UUID(address['contactId'])
        self.name = address['name']
        if 'supplement' in address:
            self.supplement = address['supplement']
        else:
            self.supplement = ""
        self.street = address['street']
        self.city = address['city']
        try:
            self.zip = int(address['zip'])
        except ValueError:
            self.zip = 0
            pass
        self.countryCode = address['countryCode']

class UnitPrice:
    currency: str
    net_amount: float
    gross_amount: float
    tax_rate_percentage: int

    def __init__(self, unit_price: dict):
        self.currency = unit_price['currency']
        self.net_amount = unit_price['netAmount']
        self.gross_amount = unit_price['grossAmount']
        self.tax_rate_percentage = unit_price['taxRatePercentage']

class LineItem:
    id: uuid.uuid4
    type: Type
    name: str
    description: str
    quantity: int
    unit_name: str
    unit_price: UnitPrice
    discount_percentage: float
    line_item_amount: float

    def __init__(self, line_item: dict):
        self.id = uuid.UUID(line_item['id'])
        try:
            self.type = Type(line_item['type'])
        except ValueError:
            self.type = Type.UNDEFINED
        self.name = line_item['name']
        self.description = line_item['description']
        self.quantity = line_item['quantity']
        self.unit_name = line_item['unitName']
        self.unit_price = UnitPrice(line_item['unitPrice'])
        self.discount_percentage = line_item['discountPercentage']
        self.line_item_amount = line_item['lineItemAmount']

class Invoice:
    id: uuid.uuid4
    organization_id: uuid.uuid4
    created_date: datetime
    updated_date: datetime
    version: int
    language: str
    archived: bool
    voucher_status: VoucherStatus
    voucher_number: str
    voucher_date: datetime
    due_date: datetime
    address: Address
    line_items: list

    def __init__(self, invoice: dict):
        self.id = uuid.UUID(invoice['id'])
        self.organization_id = uuid.UUID(invoice['organizationId'])
        self.created_date = datetime.fromisoformat(invoice['createdDate'])
        self.updated_date = datetime.fromisoformat(invoice['updatedDate'])
        self.version = invoice['version']
        self.language = invoice['language']
        self.archived = invoice['archived']
        self.voucher_status = invoice['voucherStatus']
        self.voucher_number = invoice['voucherNumber']
        self.voucher_date = datetime.fromisoformat(invoice['voucherDate'])
        self.due_date = datetime.fromisoformat(invoice['dueDate'])
        self.address = Address(invoice['address'])
        self.line_items = invoice['lineItems']

class Voucher:
    id: uuid.uuid4
    voucher_type: VoucherType
    voucher_status: VoucherStatus
    voucher_number: str
    voucher_date: datetime
    created_date: datetime
    updated_date: datetime
    due_date: datetime
    contact_id: uuid.uuid4
    contact_name: str
    total_amount: float
    open_amount: float
    currency: str
    archived: bool

    def __init__(self, voucher: dict):
        self.id = uuid.UUID(voucher['id'])
        self.voucher_type = VoucherType(voucher['voucherType'])
        self.voucher_status = VoucherStatus(voucher['voucherStatus'])
        self.voucher_number = voucher['voucherNumber']
        self.voucher_date = datetime.fromisoformat(voucher['voucherDate'])
        self.created_date = datetime.fromisoformat(voucher['createdDate'])
        self.updated_date = datetime.fromisoformat(voucher['updatedDate'])
        self.due_date = datetime.fromisoformat(voucher['dueDate'])
        if ('contactId' in voucher and voucher['contactId'] == "null") or ('contactId' not in voucher):
            self.contact_id = None
        else:
            self.contact_id = voucher['contactId']
        self.contact_name = voucher['contactName']
        self.total_amount = voucher['totalAmount']
        self.open_amount = voucher['openAmount']
        self.currency = voucher['currency']
        self.archived = voucher['archived']

class VoucherList:
    content: list[Voucher]
    first: bool
    last: bool
    total_pages: int
    total_elements: int
    number_of_elements: int
    size: int
    number: int
    sort: list

    def __init__(self, voucherlist: dict):
        self.content = []
        for voucher in voucherlist['content']:
            self.content.append(Voucher(voucher))
        self.first = voucherlist['first']
        self.last = voucherlist['last']
        self.total_pages = voucherlist['totalPages']
        self.total_elements = voucherlist['totalElements']
        self.number_of_elements = voucherlist['numberOfElements']
        self.size = voucherlist['size']
        self.number = voucherlist['number']
        self.sort = voucherlist['sort']
