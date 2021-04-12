from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.companies.company import create_account, create_company
from companies.models import Company
from companies.serializers import CompanySerializer


class CreateNewCompanyAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company_account = create_account()
        self.valid_company = {
            'account': self.company_account.id,
            'name': fake.sentence(1),
            'type': fake.random_element(Company.Type.values)
        }
        not_existing_account = 10000000
        self.invalid_company = {
            'account': not_existing_account,
            'name': fake.sentence(1),
            'type': fake.random_element(Company.Type.values)
        }
        self.company_list_url = reverse('companies:list')

    def test_valid_company_creation(self):
        response = self.client.post(self.company_list_url, self.valid_company, format='json')
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, dict(*serializer.data))

    def test_invalid_company_creation(self):
        response = self.client.post(self.company_list_url, self.invalid_company, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCompanyAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.company_detail_url = reverse('companies:detail', kwargs={'pk': self.company.account.id})

    def test_company_read(self):
        response = self.client.get(self.company_detail_url)
        serializer = CompanySerializer(self.company)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateCompanyAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()

        not_valid_value = [1, 2, 3, 4]
        not_valid_type = fake.sentence(2)

        self.valid_partial_data = {
            'name': fake.sentence(1)
        }
        self.invalid_partial_data = {
            'name': not_valid_value
        }

        self.valid_data = {
            'account': self.company.account.id,
            'name': fake.sentence(1),
            'type': fake.random_element(Company.Type.values),
        }

        self.invalid_data = {
            'account': self.company.account.id,
            'name': not_valid_value,
            'type': not_valid_type,
        }

        self.company_detail_url = reverse('companies:detail', kwargs={'pk': self.company.account.id})

    def test_valid_company_partial_update(self):
        response = self.client.patch(self.company_detail_url, self.valid_partial_data, format='json')
        self.company = Company.objects.get(pk=self.company.account.id)
        serializer = CompanySerializer(self.company)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_company_partial_update(self):
        response = self.client.patch(self.company_detail_url, self.invalid_partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_company_update(self):
        response = self.client.put(self.company_detail_url, self.valid_data, format='json')
        self.company = Company.objects.get(pk=self.company.account.id)
        serializer = CompanySerializer(self.company)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_company_update(self):
        response = self.client.patch(self.company_detail_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteCompanyAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.not_existing_company_pk = 1000000
        self.company_detail_url = reverse('companies:detail', kwargs={'pk': self.company.account.id})

    def test_valid_company_delete(self):
        response = self.client.delete(self.company_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_company_delete(self):
        response = self.client.delete(self.company_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
