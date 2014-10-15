from django.test import TestCase

import adapter
from .api import get_address_data


class AdapterTest(TestCase):

    record = get_address_data('666 Brooklyn St')

    def test_billing_account_kwargs(self):
        """
        Sanity test for adapter.billing_account_kwargs()
        """
        kwargs = adapter.billing_account_kwargs(self.record)
        self.assertIn('external_id', kwargs)
        self.assertEqual(
            kwargs['external_id'],
            self.record['account_number']
        )

    def test_billing_account_defaults(self):
        """
        Sanity test for adapter.billing_account_defaults()
        """
        defaults = adapter.billing_account_defaults(**self.record)
        for default in ('improvement_area', 'assessment'):
            self.assertIn(default, defaults)

    def test_get_or_create_account_owner(self):
        """
        Sanity test for adapter.get_or_create_account_owner()
        """
        account_owner = adapter.get_or_create_account_owner(**self.record)
        self.assertIsNotNone(account_owner.owner)

    def test_get_or_create_billing_account(self):
        """
        Sanity test for adapter.get_or_create_billing_account()
        """
        account_owner = adapter.get_or_create_account_owner(**self.record)
        billing_account = adapter.get_or_create_billing_account(self.record,
                                                                account_owner)
        self.assertEqual(billing_account.external_id, self.record['account_number'])
