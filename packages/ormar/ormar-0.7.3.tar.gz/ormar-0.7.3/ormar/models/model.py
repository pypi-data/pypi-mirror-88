import itertools
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import sqlalchemy

import ormar.queryset  # noqa I100
from ormar.exceptions import ModelPersistenceError, NoMatch
from ormar.fields.many_to_many import ManyToManyField
from ormar.models import NewBaseModel  # noqa I100
from ormar.models.metaclass import ModelMeta


def group_related_list(list_: List) -> Dict:
    test_dict: Dict[str, Any] = dict()
    grouped = itertools.groupby(list_, key=lambda x: x.split("__")[0])
    for key, group in grouped:
        group_list = list(group)
        new = [
            "__".join(x.split("__")[1:]) for x in group_list if len(x.split("__")) > 1
        ]
        if any("__" in x for x in new):
            test_dict[key] = group_related_list(new)
        else:
            test_dict[key] = new
    return test_dict


if TYPE_CHECKING:  # pragma nocover
    from ormar import QuerySet

T = TypeVar("T", bound="Model")


class Model(NewBaseModel):
    __abstract__ = False
    if TYPE_CHECKING:  # pragma nocover
        Meta: ModelMeta
        objects: "QuerySet"

    def __repr__(self) -> str:  # pragma nocover
        _repr = {k: getattr(self, k) for k, v in self.Meta.model_fields.items()}
        return f"{self.__class__.__name__}({str(_repr)})"

    @classmethod
    def from_row(  # noqa CCR001
        cls: Type[T],
        row: sqlalchemy.engine.ResultProxy,
        select_related: List = None,
        related_models: Any = None,
        previous_table: str = None,
        fields: Optional[Union[Dict, Set]] = None,
        exclude_fields: Optional[Union[Dict, Set]] = None,
    ) -> Optional[T]:

        item: Dict[str, Any] = {}
        select_related = select_related or []
        related_models = related_models or []
        if select_related:
            related_models = group_related_list(select_related)

        if (
            previous_table
            and previous_table in cls.Meta.model_fields
            and issubclass(cls.Meta.model_fields[previous_table], ManyToManyField)
        ):
            previous_table = cls.Meta.model_fields[
                previous_table
            ].through.Meta.tablename

        if previous_table:
            table_prefix = cls.Meta.alias_manager.resolve_relation_join(
                previous_table, cls.Meta.table.name
            )
        else:
            table_prefix = ""
        previous_table = cls.Meta.table.name

        item = cls.populate_nested_models_from_row(
            item=item,
            row=row,
            related_models=related_models,
            previous_table=previous_table,
            fields=fields,
            exclude_fields=exclude_fields,
        )
        item = cls.extract_prefixed_table_columns(
            item=item,
            row=row,
            table_prefix=table_prefix,
            fields=fields,
            exclude_fields=exclude_fields,
        )

        instance: Optional[T] = None
        if item.get(cls.Meta.pkname, None) is not None:
            item["__excluded__"] = cls.get_names_to_exclude(
                fields=fields, exclude_fields=exclude_fields
            )
            instance = cls(**item)
            instance.set_save_status(True)
        else:
            instance = None

        return instance

    @classmethod
    def populate_nested_models_from_row(  # noqa: CFQ002
        cls,
        item: dict,
        row: sqlalchemy.engine.ResultProxy,
        related_models: Any,
        previous_table: sqlalchemy.Table,
        fields: Optional[Union[Dict, Set]] = None,
        exclude_fields: Optional[Union[Dict, Set]] = None,
    ) -> dict:
        for related in related_models:
            if isinstance(related_models, dict) and related_models[related]:
                first_part, remainder = related, related_models[related]
                model_cls = cls.Meta.model_fields[first_part].to

                fields = cls.get_included(fields, first_part)
                exclude_fields = cls.get_excluded(exclude_fields, first_part)

                child = model_cls.from_row(
                    row,
                    related_models=remainder,
                    previous_table=previous_table,
                    fields=fields,
                    exclude_fields=exclude_fields,
                )
                item[model_cls.get_column_name_from_alias(first_part)] = child
            else:
                model_cls = cls.Meta.model_fields[related].to
                fields = cls.get_included(fields, related)
                exclude_fields = cls.get_excluded(exclude_fields, related)
                child = model_cls.from_row(
                    row,
                    previous_table=previous_table,
                    fields=fields,
                    exclude_fields=exclude_fields,
                )
                item[model_cls.get_column_name_from_alias(related)] = child

        return item

    @classmethod
    def extract_prefixed_table_columns(  # noqa CCR001
        cls,
        item: dict,
        row: sqlalchemy.engine.result.ResultProxy,
        table_prefix: str,
        fields: Optional[Union[Dict, Set]] = None,
        exclude_fields: Optional[Union[Dict, Set]] = None,
    ) -> dict:

        # databases does not keep aliases in Record for postgres, change to raw row
        source = row._row if cls.db_backend_name() == "postgresql" else row

        selected_columns = cls.own_table_columns(
            model=cls,
            fields=fields or {},
            exclude_fields=exclude_fields or {},
            use_alias=False,
        )

        for column in cls.Meta.table.columns:
            alias = cls.get_column_name_from_alias(column.name)
            if alias not in item and alias in selected_columns:
                prefixed_name = (
                    f'{table_prefix + "_" if table_prefix else ""}{column.name}'
                )
                item[alias] = source[prefixed_name]

        return item

    async def upsert(self: T, **kwargs: Any) -> T:
        if not self.pk:
            return await self.save()
        return await self.update(**kwargs)

    async def save(self: T) -> T:
        self_fields = self._extract_model_db_fields()

        if not self.pk and self.Meta.model_fields[self.Meta.pkname].autoincrement:
            self_fields.pop(self.Meta.pkname, None)
        self_fields = self.populate_default_values(self_fields)
        self.from_dict(
            {
                k: v
                for k, v in self_fields.items()
                if k not in self.extract_related_names()
            }
        )

        await self.signals.pre_save.send(sender=self.__class__, instance=self)

        self_fields = self.translate_columns_to_aliases(self_fields)
        expr = self.Meta.table.insert()
        expr = expr.values(**self_fields)

        pk = await self.Meta.database.execute(expr)
        if pk and isinstance(pk, self.pk_type()):
            setattr(self, self.Meta.pkname, pk)

        self.set_save_status(True)
        # refresh server side defaults
        if any(
            field.server_default is not None
            for name, field in self.Meta.model_fields.items()
            if name not in self_fields
        ):
            await self.load()

        await self.signals.post_save.send(sender=self.__class__, instance=self)
        return self

    async def save_related(  # noqa: CCR001
        self, follow: bool = False, visited: Set = None, update_count: int = 0
    ) -> int:  # noqa: CCR001
        if not visited:
            visited = {self.__class__}
        else:
            visited = {x for x in visited}
            visited.add(self.__class__)

        for related in self.extract_related_names():
            if self.Meta.model_fields[related].virtual or issubclass(
                self.Meta.model_fields[related], ManyToManyField
            ):
                for rel in getattr(self, related):
                    update_count, visited = await self._update_and_follow(
                        rel=rel,
                        follow=follow,
                        visited=visited,
                        update_count=update_count,
                    )
                visited.add(self.Meta.model_fields[related].to)
            else:
                rel = getattr(self, related)
                update_count, visited = await self._update_and_follow(
                    rel=rel, follow=follow, visited=visited, update_count=update_count
                )
                visited.add(rel.__class__)
        return update_count

    @staticmethod
    async def _update_and_follow(
        rel: T, follow: bool, visited: Set, update_count: int
    ) -> Tuple[int, Set]:
        if follow and rel.__class__ not in visited:
            update_count = await rel.save_related(
                follow=follow, visited=visited, update_count=update_count
            )
        if not rel.saved:
            await rel.upsert()
            update_count += 1
        return update_count, visited

    async def update(self: T, **kwargs: Any) -> T:
        if kwargs:
            self.from_dict(kwargs)

        if not self.pk:
            raise ModelPersistenceError(
                "You cannot update not saved model! Use save or upsert method."
            )

        await self.signals.pre_update.send(sender=self.__class__, instance=self)
        self_fields = self._extract_model_db_fields()
        self_fields.pop(self.get_column_name_from_alias(self.Meta.pkname))
        self_fields = self.translate_columns_to_aliases(self_fields)
        expr = self.Meta.table.update().values(**self_fields)
        expr = expr.where(self.pk_column == getattr(self, self.Meta.pkname))

        await self.Meta.database.execute(expr)
        self.set_save_status(True)
        await self.signals.post_update.send(sender=self.__class__, instance=self)
        return self

    async def delete(self: T) -> int:
        await self.signals.pre_delete.send(sender=self.__class__, instance=self)
        expr = self.Meta.table.delete()
        expr = expr.where(self.pk_column == (getattr(self, self.Meta.pkname)))
        result = await self.Meta.database.execute(expr)
        self.set_save_status(False)
        await self.signals.post_delete.send(sender=self.__class__, instance=self)
        return result

    async def load(self: T) -> T:
        expr = self.Meta.table.select().where(self.pk_column == self.pk)
        row = await self.Meta.database.fetch_one(expr)
        if not row:  # pragma nocover
            raise NoMatch("Instance was deleted from database and cannot be refreshed")
        kwargs = dict(row)
        kwargs = self.translate_aliases_to_columns(kwargs)
        self.from_dict(kwargs)
        self.set_save_status(True)
        return self
