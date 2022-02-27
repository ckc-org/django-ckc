from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from testapp.models import AModel, BModel

User = get_user_model()


class TestDefaultCreatedByMixin(APITestCase):
    TEST_TITLE_1 = 'test_title_1'
    TEST_TITLE_2 = 'test_title_2'

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(self.user)
        self.a_1 = AModel.objects.create(title=self.TEST_TITLE_1)
        self.a_2 = AModel.objects.create(title=self.TEST_TITLE_2)
        self.b = BModel.objects.create(a=self.a_1)

    def test_retrieve_renders_full_serializer_on_field(self):
        resp = self.client.get(reverse('bmodel-detail', args=(self.b.pk,)))
        assert resp.status_code == 200
        assert resp.json()['a']['title'] == self.TEST_TITLE_1

    def test_update_accepts_pk_on_field(self):
        resp = self.client.patch(
            reverse('bmodel-detail', args=(self.b.pk,)),
            {
                'a': self.a_2.pk,
            }
        )
        assert resp.status_code == 200
        assert resp.json()['a']['title'] == self.TEST_TITLE_2

    def test_field_fails_if_no_read_serializer_kwarg_passed(self):
        try:
            from testapp.misconfigured_serializers import MisconfiguredSerializer  # noqa
        except AssertionError:
            pass
        else:
            assert False, 'MisconfiguredSerializer should have raised AssertionError'
