# -*- coding: utf-8 -*-

import logging

import pytest
from django.urls import reverse

from crashlog.models import Error

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_changelist(django_app, admin_user):
    url = reverse('admin:crashlog_error_changelist')
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db
def test_display(django_app, admin_user, error):
    url = reverse('admin:crashlog_error_change', args=[error.pk])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db
def test_empty_log(django_app, admin_user, error):
    url = reverse('admin:crashlog_error_empty_log')
    res = django_app.get(url, user=admin_user)
    res = res.form.submit()
    assert res.status_code == 302
    assert not Error.objects.filter(id=error.id).exists()

