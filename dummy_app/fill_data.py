# -*- coding: utf-8 -*-

from dummy_app.models import DummyData

def fill():
    dummy_data = DummyData.objects.all().reverse()[0]
    for i in xrange(dummy_data.id, dummy_data.id + 1000):
        DummyData.objects.create(
                                 name='name %i' %i,
                                 type='type %i' %i
                                ) 