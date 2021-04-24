from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from freights.models import Freight, Rule, State
from freights.serializers import FreightSerializer, RuleSerializer, StateSerializer


class FreightListCreateAPIView(generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer


class FreightRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer


class FreightHealthCheckAPIView(views.APIView):
    def post(self, request, pk=None):
        freight = generics.get_object_or_404(Freight, pk=pk)
        if freight.damage_level > freight.DAMAGE_THRESHOLD_VALUE:
            freight.is_damaged = True
            freight.save()
        return Response({'is_damaged': freight.is_damaged})


class ReturnFreightAPIView(views.APIView):
    def post(self, request, pk=None):
        freight = generics.get_object_or_404(Freight, pk=pk)

        if not freight.transfer:
            return Response(data={'detail': 'Transfer is not assigned to the freight'},
                            status=status.HTTP_400_BAD_REQUEST)

        if freight.status not in [Freight.Status.RETURNING, Freight.Status.RETURNED]:
            freight.start_return()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data={'detail': 'Freight is already on his way to be returned'},
                        status=status.HTTP_400_BAD_REQUEST)


class RuleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RuleSerializer

    def get_queryset(self):
        freight = generics.get_object_or_404(Freight, pk=self.kwargs['pk'])
        return Rule.objects.filter(freight=freight)


class RuleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RuleSerializer

    def get_queryset(self):
        freight = generics.get_object_or_404(Freight, pk=self.kwargs['pk'])
        return Rule.objects.filter(freight=freight)

    def get_object(self):
        freight = generics.get_object_or_404(Freight, pk=self.kwargs['freight_pk'])
        return generics.get_object_or_404(Rule, pk=self.kwargs['rule_pk'], freight=freight)


class StateListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        freight = generics.get_object_or_404(Freight, pk=self.kwargs['freight_pk'])
        rule = generics.get_object_or_404(Rule, pk=self.kwargs['rule_pk'], freight=freight)
        return State.objects.filter(rule=rule)


class StateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        freight = generics.get_object_or_404(Freight, pk=self.kwargs['freight_pk'])
        rule = generics.get_object_or_404(Rule, pk=self.kwargs['rule_pk'], freight=freight)
        return State.objects.filter(rule=rule)

    def get_object(self):
        freight = generics.get_object_or_404(Freight, pk=self.kwargs['freight_pk'])
        rule = generics.get_object_or_404(Rule, pk=self.kwargs['rule_pk'], freight=freight)
        return generics.get_object_or_404(State, pk=self.kwargs['state_pk'], rule=rule)
