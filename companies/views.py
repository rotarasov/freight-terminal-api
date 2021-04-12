from rest_framework import generics

from companies.models import Company, Robot, Service
from companies.serializers import CompanySerializer, RobotSerializer, ServiceSerializer


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class RobotListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RobotSerializer

    def get_queryset(self):
        company = generics.get_object_or_404(Company, pk=self.kwargs['pk'])
        return Robot.objects.filter(company=company)


class RobotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer

    def get_object(self):
        company = generics.get_object_or_404(Company, pk=self.kwargs['company_pk'])
        return generics.get_object_or_404(Robot, pk=self.kwargs['robot_pk'], company=company)


class ServiceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        company = generics.get_object_or_404(Company, pk=self.kwargs['company_pk'])
        robot = generics.get_object_or_404(Robot, pk=self.kwargs['robot_pk'], company=company)
        return Service.objects.filter(robot=robot)

    def perform_create(self, serializer):
        service = serializer.save()
        service.robot.start_transit()
        service.robot.save()


class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_object(self):
        company = generics.get_object_or_404(Company, pk=self.kwargs['company_pk'])
        robot = generics.get_object_or_404(Robot, pk=self.kwargs['robot_pk'], company=company)
        return generics.get_object_or_404(Service, pk=self.kwargs['service_pk'], robot=robot)
