from .apibase import ApiBase
from .onboard_merchant import OnboardMerchant
import json


class BusinessClientCore(ApiBase, OnboardMerchant):

    def register_customer(self, reference_number,customer_firstname,
                          customer_lastname, customer_phonenumber,
                          customer_email, customer_date_of_birth ):
        """
                 Register Customer

                 Parameters
                 ----------
                 reference_number : string
                     reference_number: A unique reference
                     number provided by the business

                 customer_firstname : string
                     customer_firstname: The first name of the customer

                 customer_lastname: string
                     customer_lastname: The last name of the customer

                 customer_phonenumber: string
                     customer_phonenumber: The phone number of the new customer.
                                          This number must not belong to an existing registered customer

                 customer_email: string
                    customer_email: The email of the new customer

                 customer_date_of_birth:
                        customer_date_of_birth: Birth date of the customer
             """

        endpoint = 'paga-webservices/business-rest/secured/registerCustomer'

        url = self._server_url() + endpoint

        pattern = reference_number + customer_phonenumber + customer_firstname + customer_lastname

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'customerFirstName': customer_firstname,
                'customerPhoneNumber': customer_phonenumber,
                'customerLastName': customer_lastname,
                'customerEmail': customer_email,
                'customerDateOfBirth': customer_date_of_birth}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def money_transfer(self, reference_number, amount, currency,
                       destination_account, destination_bank,
                       sender_principal, sender_credentials,
                       withdrawal_code, source_of_funds,
                       transaction_reference,
                       suppress_recipient_message, locale,
                       alternate_sender_name,
                       mini_recipient_kyc, holding_period):
        """
            Money Transfer

            Parameters
            ----------
            reference_number : string
                reference_number: A unique reference
                number provided by the business

            amount : double
                amount: The amount of money to
                transfer to the recipient

            currency: string
                currency: The currency of the operation,
                        if being executed in a foreign currency
            destination_account: string
                destination_account: The account identifier for
                            the recipient receiving the money transfer.

            destination_bank: For money transfers to a bank account,
                              this is the destination bank code

            sender_principal:
                   Returns
                   -------
                   JSON Object
                       JSON Object with the details of th transaction
        """

        endpoint = 'paga-webservices/business-rest/secured/moneyTransfer'

        url = self._server_url() + endpoint

        pattern = reference_number + amount + destination_account

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationAccount': destination_account,
                'destinationBank': destination_bank,
                'senderPrincipal': sender_principal,
                'senderCredentials': sender_credentials,
                'withdrawalCode': withdrawal_code,
                'sourceOfFunds': source_of_funds,
                'transferReference': transaction_reference,
                'suppressRecipientMessage': suppress_recipient_message,
                'locale': locale,
                'alternateSenderName': alternate_sender_name,
                'minRecipientKYCLevel': mini_recipient_kyc,
                'holdingPeriod': holding_period}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def airtime_purchase(self, reference_number, amount, currency,
                         destination_number, purchaser_principal,
                         purchaser_credentials, source_of_funds, locale):
        endpoint = 'paga-webservices/business-rest/secured/airtimePurchase'

        url = self._server_url() + endpoint

        pattern = reference_number + amount + destination_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationPhoneNumber': destination_number,
                'purchaserPrincipal': purchaser_principal,
                'purchaser_principal': purchaser_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_merchants(self, reference_number, locale):
        endpoint = 'paga-webservices/business-rest/secured/getMerchants'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_merchant_services(self, reference_number,
                              merchant_public_id, locale):
        endpoint = 'paga-webservices/business-rest/secured/getMerchantServices'

        url = self._server_url() + endpoint

        pattern = reference_number + merchant_public_id

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'merchantPublicId': merchant_public_id,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_banks(self, reference_number, locale):
        endpoint = 'paga-webservices/business-rest/secured/getBanks'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def account_balance(self, reference_number, acct_principal,
                        acct_credentials, source_of_funds, locale):
        endpoint = 'paga-webservices/business-rest/secured/accountBalance'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'accountPrincipal': acct_principal,
                'accountCredentials': acct_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def merchant_payment(self, reference_number, amount, currency,
                         merchant_account, merchant_reference_number,
                         merchant_service, purchaser_principal,
                         purchaser_credentials, source_of_funds,
                         locale):
        endpoint = 'paga-webservices/business-rest/secured/merchantPayment'

        url = self._server_url() + endpoint

        pattern = reference_number + amount + merchant_account \
                  + merchant_reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'merchantAccount': merchant_account,
                'merchantReferenceNumber': merchant_reference_number,
                'merchantService': merchant_service,
                'purchaserPrincipal': purchaser_principal,
                'purchaserCredentials': purchaser_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_operation_status(self, reference_number, locale):
        endpoint = 'paga-webservices/business-rest/secured/getOperationStatus'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_mobile_operators(self, reference_number, locale):
        endpoint = 'paga-webservices/business-rest/secured/getMobileOperators'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def validate_deposit_to_bank(self, reference_number, amount,
                                 currency, destination_bank_uuid,
                                 destination_bank_acct_no,
                                 recipient_phone_number,
                                 recipient_mobile_operator_code,
                                 recipient_email, recipient_name,
                                 locale):
        endpoint = 'paga-webservices/business-rest/secured' \
                   '/validateDepositToBank'

        url = self._server_url() + endpoint

        pattern = reference_number + amount + destination_bank_uuid \
                  + destination_bank_acct_no

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationBankUUID': destination_bank_uuid,
                'destinationBankAccountNumber': destination_bank_acct_no,
                'recipientPhoneNumber': recipient_phone_number,
                'recipientMobileOperatorCode': recipient_mobile_operator_code,
                'recipientEmail': recipient_email,
                'recipientName': recipient_name,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def deposit_to_bank(self, reference_number, amount, currency,
                        destination_bank_uuid, destination_bank_acct_no,
                        recipient_phone_number,
                        recipient_mobile_operator_code,
                        recipient_email, recipient_name,
                        locale):
        endpoint = 'paga-webservices/business-rest/secured/depositToBank'

        url = self._server_url() + endpoint

        pattern = reference_number + amount + destination_bank_uuid \
                  + destination_bank_acct_no

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationBankUUID': destination_bank_uuid,
                'destinationBankAccountNumber': destination_bank_acct_no,
                'recipientPhoneNumber': recipient_phone_number,
                'recipientMobileOperatorCode':
                    recipient_mobile_operator_code,
                'recipientEmail': recipient_email,
                'recipientName': recipient_name,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def transaction_history(self, reference_number,
                            acct_principal,
                            acct_credentials,
                            start_date, end_date, locale):
        endpoint = 'paga-webservices/business-rest/secured/transactionHistory'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'accountPrincipal': acct_principal,
                'accountCredentials': acct_credentials,
                'startDateUTC': start_date,
                'endDateUTC': end_date,
                'locale': locale}

        json_data = json.dumps(data)

        assert isinstance(generated_hash, object)
        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def recent_transaction_history(self, reference_number, acct_principal,
                                   acct_credentials, locale):
        endpoint = 'paga-webservices/business-rest/secured/transactionHistory'

        url = self._server_url() + endpoint

        pattern = reference_number

        generated_hash = self._generate_hash(pattern)

        data = {'referenceNumber': reference_number,
                'accountPrincipal': acct_principal,
                'accountCredentials': acct_credentials,
                'locale': locale}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_merchant_account_details(self, reference_number,
                                     merchant_account,
                                     merchant_reference_number,
                                     merchant_service_product_code):
        endpoint = 'paga-webservices/business-rest/secured' \
                   '/getMerchantAccountDetails'

        url = self._server_url() + endpoint

        pattern = reference_number \
                  + merchant_account \
                  + merchant_reference_number \
                  + merchant_service_product_code

        generated_hash = self._generate_hash(pattern)

        data = {'merchantReferenceNumber': merchant_reference_number,
                'merchantAccount': merchant_account,
                'referenceNumber': reference_number,
                'merchantServiceProductCode':
                    merchant_service_product_code}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def bulk_money_transfer(self, money_transfer_items, bulk_reference_number):
        endpoint = 'paga-webservices/business-rest/secured' \
                   '/moneyTransferBulk'

        url = self._server_url() + endpoint

        pattern = money_transfer_items[0]['referenceNumber'] +\
                  str(money_transfer_items[0]['amount']) \
                  + money_transfer_items[0]['destinationAccount'] \
                  + str(len(money_transfer_items))

        generated_hash = self._generate_hash(pattern)

        data = {'items': money_transfer_items,
                'bulkReferenceNumber': bulk_reference_number}

        json_data = json.dumps(data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def onboard_merchant(self, reference_number, merchant_external_id,
                         name, description, address_line1, address_line2,
                         address_city, address_state, address_zip,
                         address_country, first_name, last_name, date_of_birth,
                         phone, email, established_date, website_url,
                         display_name, type, finance_admin_email):
        endpoint = "paga-webservices/business-rest/secured/onboardMerchant"

        url = self._server_url() + endpoint

        data = {}

        merchant_info = self.build_merchant_info(name, description,
                                                 address_line1, address_line2,
                                                 address_city, address_state, address_zip,
                                                 address_country, first_name,
                                                 last_name, date_of_birth,
                                                 phone, email, established_date,
                                                 website_url, display_name)

        integration = self.build_integration_properties(type,
                                                        finance_admin_email)

        pattern = reference_number + merchant_external_id \
                  + name + phone + email

        generated_hash = self._generate_hash(pattern)

        data['reference'] = reference_number
        data['merchantExternalId'] = merchant_external_id
        data['integration'] = integration
        data['merchantInfo'] = merchant_info

        print(data)

        json_data = json.dumps(data)

        print(json_data)

        response = self._post_request('POST', url, generated_hash, json_data)

        return response

    def get_transactions(self, *args):
        list_of_transactions = []

        for transaction_elements in args:
            transactions = {
                "referenceNumber": transaction_elements[0],
                "amount": transaction_elements[1],
                "currency": transaction_elements[2],
                "destinationAccount": transaction_elements[3],
                "destinationBank": transaction_elements[4],
                "transferReference": transaction_elements[5],
                "sourceOfFunds": transaction_elements[6],
                "sendWithdrawalCode": transaction_elements[7],
                "suppressRecipientMessage": transaction_elements[8],
                "minRecipentKYCLevel": transaction_elements[9],
                "holdingPeriod": transaction_elements[10]
            }

            list_of_transactions.append(transactions)

        print(len(list_of_transactions))

        return list_of_transactions
