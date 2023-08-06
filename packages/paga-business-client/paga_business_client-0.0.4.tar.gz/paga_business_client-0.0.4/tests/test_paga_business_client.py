from unittest import TestCase

from paga_business_library.src.paga_business_client import BusinessClientCore

class TestBusinessClientCore(TestCase):

    def setUp(self):
        super(TestBusinessClientCore, self).setUp()
        self.business_client_core = BusinessClientCore('98F32858-CC3B-42D4-95A3-742110A8D405',
                                                   'rR9@f8u@bBES',
                                                   True, 'd98076e2d14c4045970edc466faa2ec8cc47c9b89b654001b5e4db27179a0b9559bee92b78034c558a9d24aca2fa4135db8938a3f4a74b7da1157dee68e15213')

    def test_money_transfer(self):
        response = self.business_client_core.money_transfer("3325626", "110", "NGN", "+2348060075922", None, None,
                                                       None, True, None, None, None, "NG", None, None, None)

        print(response)

        self.assertIsNotNone(response, True)

    def test_airtime_purchase(self):
        response = self.business_client_core.airtime_purchase("45363772", "500", "NGN",
                                                              "08060075922", None, None, None, "NG")

        print(response)

        self.assertIsNotNone(response, True)

    def test_register_customer(self):
        response = self.business_client_core.register_customer("3453627211", "Babs1", "Owo1", "08090134578",
                                                               "josingowo@gmail.com", "1987-01-10")

        print(response)

        self.assertIsNotNone(response, True)

    def test_get_merchants(self):
        response = self.business_client_core.get_merchants("56377383", "en")

        print(response)

        self.assertIsNotNone(response, True)

    def test_get_merchant_services(self):
        response = self.business_client_core.get_merchant_services("45362772",
                                                                   "8E7485D9-1A67-4205-A49D-691E5B78C20D",
                                                                   "NG")

        print(response)

        self.assertIsNotNone(response, True)

    def test_get_banks(self):
        response = self.business_client_core.get_banks("2342425", "NG")

        print(response)

        self.assertIsNotNone(response, True)

    def test_account_balance(self):
        response = self.business_client_core.account_balance("243783893", None, None, None, "NG")

        print(response)

        self.assertIsNotNone(response, True)

    def test_merchant_payment(self):
        services = ["ACCACC101"]

        response = self.business_client_core.merchant_payment("3425626",  "1500",
                                                              "NGN" ,"A3878DC1-F07D-48E7-AA59-8276C3C26647",
                                                              "4100029992", services, None, None, None , "NG")

        print(response)

        self.assertIsNotNone(response,True)

    def test_get_operation_status(self):

        response = self.business_client_core.get_operation_status("3425626", "NG")

        print(response)

        self.assertIsNotNone(response, True)


    def test_get_mobile_operators(self):

        response = self.business_client_core.get_mobile_operators("5363773", "NG")

        print(response)

        self.assertIsNotNone(response,True)

    def test_validate_deposit_to_bank(self):

        response = self.business_client_core\
            .validate_deposit_to_bank("335637828", "1000", "NGN",
                                      "3E94C4BC-6F9A-442F-8F1A-8214478D5D86","2200000002",None,
                                      None, None, None, "NG")

        print(response)

        self.assertIsNotNone(response, True)

    def test_deposit_to_bank(self):

        response = self.business_client_core \
            .deposit_to_bank("5637828", "2000", "NGN",
                                      "3E94C4BC-6F9A-442F-8F1A-8214478D5D86", "2200000002", None,
                                      None, None, None, "NG")
        print(response)

        self.assertIsNotNone(response, True)

    def  test_transaction_history(self):

        response = self.business_client_core.transaction_history("453627282",None, None,
                                                                 "2020-03-03", "2020-04-04", "NG")

        print (response)

        self.assertIsNotNone(response, True)

    def  test_recent_transaction_history(self):

        response = self.business_client_core.recent_transaction_history("453627282",None, None,'' "NG")

        print (response)

        self.assertIsNotNone(response, True)

    def test_get_merchant_account_details(self):

        response = self.business_client_core\
            .get_merchant_account_details("536782882",
                                          "8E7485D9-1A67-4205-A49D-691E5B78C20D",
                                          "4100029992", "PrePre101")

        print (response)

        self.assertIsNotNone(response, True)

    def test_money_transfer_bulk(self):

        items = self.business_client_core.get_transactions(
            ['2778229', 1500, 'NGN', '08030408527', None, '45367893', None, None, None, 'KYC1', 30],
            ['7882281', 1000, 'NGN', '08032003066', None, '41567893', None, None, None, 'KYC1', 30],
            ['8782281', 2000, 'NGN', '08060075922', None, '45163789', None, None, None, 'KYC1', 30])

        response = self.business_client_core.bulk_money_transfer(items ,"789w9w89")

        print(response)

        self.assertIsNotNone(response, True)

    def test_onboard_merchant(self):

        response = self.business_client_core.onboard_merchant("3536625636","7383920020202","CWDF",
                                                         "Computers","festac","satellite","Lagos", "Lagos", "23401","Nigeria","james",
                                                         "homie","1992-07-05T00:00:00.000Z","09030030090","babs.owolabi@icloud.com",
                                                         "1992-07-05T00:00:00.000Z","www.james.com","Babs", "EMAIL_NOTIFICATION","ba@a.com")

        print (response)

        self.assertIsNotNone(response, True)
