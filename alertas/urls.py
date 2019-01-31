from django.urls import path

from . import views, old_views

urlpatterns = [
    path('alertas/', views.MyAccountView.as_view(), name='dashboard-index'),
    path('alertas/profile/', views.ProfileView.as_view(), name='alertas-profile'),
    path('alertas/events/', views.AlertaEventsView.as_view(), name='alertas-events'),
    path('alertas/service/follow/', views.ServiceAlertaView.as_view(), name='service-follow'),
    path('alertas/service/api/', views.ServiceAPIView.as_view(), name='service-api'),
    path('alertas/service/subscriptions/', views.ServiceSubscriptionView.as_view(), name='service-subscriptions'),
    path('alertas/billing/', views.BillingView.as_view(), name='alertas-billing'),
    path('alertas/payment/', views.PaymentView.as_view(), name='alertas-payment'),
    path('alertas/payment/new_card/', views.add_card, name='alertas-payment-add-card'),
    path('alertas/payment/checkout/', views.checkout, name="checkout_page"),
    path('alertas/payment/checkout2/', views.checkout_existing_card, name="checkout_existing"),
    path('alertas/new/acto/', views.alerta_acto_create, name='alertas-new-acto'),
    path('alertas/history/', views.DashboardHistoryView.as_view(), name='alertas-history'),
    path('alertas/remove/acto/<id>/', views.alerta_remove_acto, name='alerta-remove-acto'),
    path('alertas/ayuda/', views.DashboardSupportView.as_view(), name='alertas-ayuda'),
    path('alertas/cart/', views.CartView.as_view(), name='alertas-cart'),
    path('alertas/cart/buy/<product>/', views.add_to_cart, name='buy-product'),
    path('alertas/cart/removecart/', views.remove_cart, name='alertas-removecart'),
    path('alertas/settings/update/billing/', views.settings_update_billing, name='alertas-settings-billing'),
    path('alertas/history/download/<id>/', views.download_alerta_history_csv, name='alerta-history-download'),
    path('alertas/<id>/', views.AlertaDetailView.as_view(), name='alertas-detail'),

    path('old/alertas/', old_views.MyAccountView.as_view(), name='old-dashboard-index'),
    path('old/alertas/events/', old_views.AlertaEventsView.as_view(), name='old-alertas-events'),
    path('old/alertas/service/follow/', old_views.ServiceAlertaView.as_view(), name='old-service-follow'),
    path('old/alertas/service/api/', old_views.ServiceAPIView.as_view(), name='old-service-api'),
    path('old/alertas/service/subscriptions/', old_views.ServiceSubscriptionView.as_view(), name='old-service-subscriptions'),
    path('old/alertas/billing/', old_views.BillingView.as_view(), name='old-alertas-billing'),
    path('old/alertas/payment/', old_views.PaymentView.as_view(), name='old-alertas-payment'),
    path('old/alertas/payment/new_card/', old_views.add_card, name='old-alertas-payment-add-card'),
    path('old/alertas/payment/checkout', old_views.checkout, name="old-checkout_page"),
    path('old/alertas/payment/checkout2', old_views.checkout_existing_card, name="old-checkout_existing"),
    path('old/alertas/new/acto/', old_views.alerta_acto_create, name='old-alertas-new-acto'),
    path('old/alertas/history/', old_views.DashboardHistoryView.as_view(), name='old-alertas-history'),
    path('old/alertas/remove/acto/<id>/', old_views.alerta_remove_acto, name='old-alerta-remove-acto'),
    path('old/alertas/ayuda/', old_views.DashboardSupportView.as_view(), name='old-alertas-ayuda'),
    path('old/alertas/cart', old_views.CartView.as_view(), name='old-alertas-cart'),
    path('old/alertas/cart/buy/<product>', old_views.add_to_cart, name='old-buy-product'),
    path('old/alertas/cart/removecart', old_views.remove_cart, name='old-alertas-removecart'),
    path('old/alertas/settings/update/billing/', old_views.settings_update_billing, name='old-alertas-settings-billing'),
    path('old/alertas/history/download/<id>/', old_views.download_alerta_history_csv, name='old-alerta-history-download'),
    path('old/alertas/<id>/', old_views.AlertaDetailView.as_view(), name='old-alertas-detail'),
#    url(r'^(?P<id>\d+)/$', views.alertas_view, name='alertas-detail'),

    # AJAX
    path('alertas/suggest_company/', views.suggest_company, name='suggest_company'),
    path('alertas/suggest_person/', views.suggest_person, name='suggest_person'),
    path('alertas/remove_card/', views.remove_card, name='remove_card'),
    path('alertas/set_default_card/', views.set_default_card, name='set_default_card'),

    path('ajax/follow/', views.ajax_follow, name='borme-ajax-follow'),
]
