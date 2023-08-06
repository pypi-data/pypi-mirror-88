class OnboardMerchant(object):

    def build_merchant_info(self, name, description,
                            address_line1, address_line2,
                            address_city, address_state,
                            address_zip, address_country,
                            first_name, last_name,
                            date_of_birth, phone, email,
                            established_date, website_url,
                            display_name):
        merchant_info = {}

        merchant_info['legalEntity'] = \
            self.build_legal_entity(name, description,
                                    address_line1, address_line2,
                                    address_city, address_state,
                                    address_zip, address_country)

        merchant_info['legalEntityRepresentative'] = \
            self.build_legal_entity_representative(first_name,
                                                   last_name,
                                                   date_of_birth,
                                                   phone,
                                                   email)

        merchant_info['additionalParameters'] = \
            self.build_additional_parameters(established_date,
                                             website_url,
                                             display_name)

        return merchant_info

    def build_legal_entity(self, name, description,
                           address_line1, address_line2,
                           address_city, address_state,
                           address_zip, address_country):
        legalEntity = {'name': name,
                       'description': description,
                       'addressLine1': address_line1,
                       'addressLine2': address_line2,
                       'addressCity': address_city,
                       'addressState': address_state,
                       'addressZip': address_zip,
                       'addressCountry': address_country}

        return legalEntity

    def build_legal_entity_representative(self, first_name, last_name,
                                          date_of_birth, phone, email):
        legalEntityRepresentative = {'firstName': first_name,
                                     'lastName': last_name,
                                     'dateOfBirth': date_of_birth,
                                     'phone': phone, 'email': email}

        return legalEntityRepresentative

    def build_additional_parameters(self, established_date,
                                    website_url, display_name):
        additional_parameters = {'establishedDate': established_date,
                                 'websiteUrl': website_url,
                                 'displayName': display_name}

        return additional_parameters

    def build_integration_properties(self, type, finance_admin_email):
        integration = {'type': type,
                       'financeAdminEmail': finance_admin_email}

        return integration
