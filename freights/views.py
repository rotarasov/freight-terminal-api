from rest_framework import generics

from freights.models import Freight, Rule, State
from freights.serializers import FreightSerializer, RuleSerializer, StateSerializer


class FreightListCreateAPIView(generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer


class FreightRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer


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

    def perform_create(self, serializer):
        state = serializer.save()
        if state.rule.is_violated():
            state.rule.freight.is_damaged = True
            state.rule.freight.save()
            state.rule.freight.return_damage_freight()


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
