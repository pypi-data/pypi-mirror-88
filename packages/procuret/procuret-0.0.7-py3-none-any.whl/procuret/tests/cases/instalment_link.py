"""
Procuret Python
Exercise Instalment Link Test
author: hugh@blinkybeach.com
"""
from procuret.tests.variants.with_supplier import TestWithSupplier
from procuret.tests.test_result import Success, TestResult
from procuret.instalment_link import InstalmentLink, InstalmentLinkOpen
from procuret.session import Session, Perspective
from procuret.ancillary.communication_option import CommunicationOption
from decimal import Decimal


class ExerciseInstalmentLink(TestWithSupplier):

    NAME = 'Create, retrieve and mark an InstalmentLink as opened'

    def execute(self) -> TestResult:

        session = Session.create_with_email(
            email=self.email,
            plaintext_secret=self.secret,
            perspective=Perspective.SUPPLIER
        )

        link = InstalmentLink.create(
            supplier=self.supplier_id,
            invoice_amount=Decimal('422.42'),
            invitee_email='noone@procuret-test-domain.org',
            invoice_identifier='Test 42',
            communication=CommunicationOption.EMAIL_CUSTOMER,
            session=session
        )

        assert isinstance(link, InstalmentLink)

        r_link = InstalmentLink.retrieve(
            public_id=link.public_id,
            session=session
        )

        assert isinstance(r_link, InstalmentLink)
        assert r_link.public_id == link.public_id

        InstalmentLinkOpen.create(
            link_id=r_link.public_id,
            session=session
        )

        o_link = InstalmentLink.retrieve(
            public_id=r_link.public_id,
            session=session
        )

        assert isinstance(o_link, InstalmentLink)
        assert len(o_link.opens) > 0
        assert isinstance(o_link.opens[0], InstalmentLinkOpen)

        return Success()
