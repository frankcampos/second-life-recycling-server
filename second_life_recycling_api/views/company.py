from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from second_life_recycling_api.models import User, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyView(ViewSet):
    def list(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def create(self, request):
        user=User.objects.get(id=request.data['user'])
        company = Company.objects.create(
            business_name=request.data['business_name'],
            phone_number=request.data['phone_number'],
            location=request.data['location'],
            user=user
        )
        company.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        company.business_name = request.data['business_name']
        company.phone_number = request.data['phone_number']
        company.location = request.data['location']
        company.user = request.data['user']
        company.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
