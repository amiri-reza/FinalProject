from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
import stripe
from transactions_app.models import UserAccountProfile
from stock_prediction.settings import STRIPE_API_KEY


@receiver
def _on_update_user(sender, instance, created, **kwargs):
    if created:
        stripe.api_key = STRIPE_API_KEY
        user_account = stripe.Customer.create(
            email=instance.email,
            name=instance.get_full_name(),
            metadata={"user_id": instance.pk, "username": instance.username},
            description="Created from Django",
        )

        profile = UserAccountProfile.objects.create(
            user=instance, stripe_customer_id=user_account.id
        )
        profile.save()
