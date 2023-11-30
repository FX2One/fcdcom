import stripe
from django.conf import settings
from django.db import models

from fcdcom.utils.models import BaseModel


# Create your models here.
class PlowingService(BaseModel):
    name = models.CharField(max_length=255, default="Plowing Service", unique=True)
    provider = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PlowingRequest(BaseModel):
    service = models.ForeignKey("PlowingService", on_delete=models.CASCADE)
    requestor = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="requestor")
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("completed", "Completed"),
        ],
        default="pending",
    )

    def charge_customer(self) -> bool:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            invoice = stripe.Invoice.create(
                customer=self.requestor.stripe_customer_id,
                auto_advance=True,
                collection_method="charge_automatically",
            )
            stripe.InvoiceItem.create(
                customer=self.requestor.stripe_customer_id,
                amount=int(self.service.price * 100),
                description=self.service.name,
                currency="eur",
                invoice=invoice.id,
            )

            # Finalize the invoice to transition it from draft to open
            """finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)

            # Attempt to pay the invoice immediately
            # If the invoice is set to be paid automatically, this will attempt the charge
            stripe.Invoice.pay(finalized_invoice.id)"""

            self.status = "completed"
            self.save()
            return True
        except Exception as e:
            return False

    def __str__(self):
        return f"{self.service.name} - {self.requestor.username}"
