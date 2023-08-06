import django_tables2 as tables
from django_tables2.utils import Accessor
from utilities.tables import BaseTable, ToggleColumn

from .models import Actor


class ActorTable(BaseTable):
    pk = ToggleColumn()
    id = tables.LinkColumn(
        viewname='plugins:conectividadeapp:actor',
        args=[Accessor('id')]
    )

    class Meta(BaseTable.Meta):
        model = Actor
        fields = (
            'pk',
            'id',
            'name',
            'telephone',
            'cellphone',
            'email',
        )