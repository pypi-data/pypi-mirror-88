import collections
import os
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, unique
from typing import List, Dict, Any
from collections.abc import Iterable, Collection
from itertools import product
from .orderedset import OrderedSet

import numpy as np
import pandas as pd

"""
This module allows you to construct a condition object in a pythonic way for pandas datafame query,parquet partition filtering and sql generation.

A condition can have the following forms:
1. a field based condition which compares one field with some value(s). It supports all comparision operators (<,<=,>,>=,==,!=)
    and also 'in' and 'not in' set membership check. It can format correctly common data types such as strings,
    iterable (for "in" and "not in") and dates. All other types are formatted as is.
2. an "and" condition comprised of a list of sub conditions;
3. an "or" condition comprised of a list of sub conditions.

The condition can then be used in the following contexts:
1. df.query conditions
2. sql where conditions
3. pyarrow or pandas.read_parquet filters

"""


@unique
class Operator(Enum):
    LE = "<="
    LT = "<"
    GE = ">="
    GT = ">"
    EQ = "="
    NEQ = "!="
    IN = "in"
    NOT_IN = "not in"


class Field:
    def __init__(self, name: str):
        self.name = name

    def __le__(self, other):
        return FieldCondition(self, Operator.LE, other)

    def __lt__(self, other):
        return FieldCondition(self, Operator.LT, other)

    def __eq__(self, other):
        if isinstance(other, str) or not isinstance(other, Collection):
            return FieldCondition(self, Operator.EQ, other)
        else:
            return FieldCondition(self, Operator.IN, self._get_collection(other))

    def __ne__(self, other):
        if isinstance(other, str) or not isinstance(other, Collection):
            return FieldCondition(self, Operator.NEQ, other)
        else:
            return FieldCondition(self, Operator.NOT_IN, self._get_collection(other))

    def __ge__(self, other):
        return FieldCondition(self, Operator.GE, other)

    def __gt__(self, other):
        return FieldCondition(self, Operator.GT, other)

    def _get_collection(self, val):
        if not (isinstance(val, Collection)):
            raise TypeError("'%s' object is not a collection", type(val).__name__)
        if len(val) == 0:
            raise ValueError("Cannot use empty collection as filter value")
        if len({type(item) for item in val}) != 1:
            raise ValueError(
                "All elements of the collection '%s' must be" " of same type", val
            )
        values = OrderedSet(val)
        return values

    def __repr__(self) -> str:
        return self.name


class FieldList:
    """
    Exposes each of the list as a field attribute which can then be used to construct field conditions.
    """

    def __init__(self, fields: List[str]):
        self._fields = fields
        for name in sorted(fields):
            setattr(self, name, Field(name))

    @classmethod
    def from_df(cls, df: pd.DataFrame):
        """A shortcut to construct a field list from the index names and columns of the dataframe"""
        return FieldList(list(df.index.names) + list(df.columns))

    def __repr__(self) -> str:
        return "FieldList [" + ",".join(self._fields) + "]"


# global constants and func for visualization
FIELD_COND_COLOR = "cyan3"
AND_COLOR = "coral"
OR_COLOR = "burlywood"


def id_gen() -> str:
    id = 1
    while True:
        yield str(id)
        id += 1


global_id = id_gen()


class Condition(ABC):
    def __init__(self):
        self.params = {}

    def set_param(self, name: str, val):
        """Sets additional param/value to pass to the end consumer. For example,
        the params can be used in sql templates.
        Note that only the top condition's params is used.

        :param name: the param name. It will be available in jinja2 SQL template.
        :param val: the value
        """
        self.params[name] = val

    def __and__(self, other):
        """Supports `&` operator which results in an `And` condition"""
        if isinstance(self, And):
            self.add(other)
            return self
        else:
            cond = And()
            cond.add(self)
            cond.add(other)
            return cond

    def empty(self):
        return False

    def __or__(self, other):
        """Supports `|` operator which results in an `Or` condition"""
        if isinstance(self, Or):
            self.add(other)
            return self
        else:
            cond = Or()
            cond.add(self)
            cond.add(other)
            return cond

    @abstractmethod
    def to_sql_where_condition(
        self, db_map: Dict[str, str] = None, indent: int = 1
    ) -> str:
        """
        Generates a string representing the condition for used in a sql where clause.

        :param db_map: map from a field name to a db field name. Note that you can also
            pass in alias in the db field name. By default, use field names directly.
        :return: condition string for sql where clause.
        """
        raise NotImplementedError()

    def get_all_field_conditions(self):
        """
        Returns all ``FieldCondition`` contained in this condition.

        :return: a dict: field name -> list of ``FieldCondition`` for this field.
        """
        visited = set()
        d = collections.defaultdict(list)

        def dfs(cond):
            visited.add(cond)
            if isinstance(cond, CompositeCondition):
                for s in cond.conditions:
                    if s not in visited:
                        dfs(s)
            else:
                d[cond.field.name].append(cond)

        dfs(self)
        return d

    def _to_sql_dict(self) -> Dict[str, str]:
        """
        Generates a dict for `SQL with individual clauses<(usage.html#sql-with-individual-clauses)>`_.
        :return: a dict: <individual field reference> -> <value str>.
        """
        id = 1
        d: Dict[str, str] = {}
        for _, fc_list in self.get_all_field_conditions().items():
            for cond in fc_list:
                field_name = cond.field.name + "_" + cond.op.name
                if field_name in d:
                    field_name += "_" + str(id)
                    id += 1
                d[field_name] = cond._query_val()
        return d

    def to_sql_dict(self, dbmap=None) -> Dict[str, Any]:
        """
        Generates a dict to pass into a sql template.

        Before you write your sql template, you can call this method and print out the dict (keys) to get an idea of
        what are available to use in your sql template.

        See also `usage examples <usage.html#sql-with-individual-clauses>`_.

        :param dbmap: to map to the actual db field name (optionally with alias) when generating "where_condition"
        :return: the dict
        """
        kwargs = self._to_sql_dict()
        kwargs["where_condition"] = self.to_sql_where_condition(dbmap)
        kwargs["condition"] = self
        kwargs.update(self.params)
        return kwargs

    @abstractmethod
    def to_df_query(self) -> str:
        """
        :return: a string representing the condition to be used in df.query()
        """
        raise NotImplementedError()

    def query(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Queries the passed in dataframe with this condition.

        :param df: the dataframe to perform query. Each field in the condition must match a columns
            or an index level in the data frame.
        :return: a dataframe whose rows satisfy this condition.
        """
        if self.empty():
            return df
        else:
            return df.query(self.to_df_query())

    @abstractmethod
    def _to_pyarrow_filter(self):
        raise NotImplementedError()

    @abstractmethod
    def eval(self, record_dict: Dict, type_conversion: bool = False) -> bool:
        """
        Evaluates the condition against the record to a bool of True of False.

        :param record_dict: a dict from a field to a value. Used to test ``FieldCondition``.
        :param type_conversion: if True, convert value in record_dict to the ``FieldCondition``
                                value type before comparision. Sometimes such conversion
                                is needed, for example, in pyarrow partition filtering.
        """
        raise NotImplementedError()

    def normalize(self):
        """
        Normalizes the condition to be one of the following:

        - a ``FieldCondition``
        - an ``And`` with a list of sub ``FieldCondition``
        - an ``Or`` with a list of sub conditions as defined above.

        In some cases, e.g., pyarrow filtering, the above restrictions must be followed.
        Any condition can be normalized to the above form in an equalivent way.

        For example, ``(a | b) & (c | d) & e`` will be normalized to
        ``(a & c & e) | (a & d & e) | (b & c & e) | (b & d& e)``.

        :return: an equivalent normalized condition.
        """
        if isinstance(self, FieldCondition):
            return self
        subs = [sub.normalize() for sub in self.conditions]
        if isinstance(self, Or):
            return Or(subs)
        # And: FieldConditions, And, Or
        or_list = []
        field_list = []
        for sub in subs:
            if isinstance(sub, FieldCondition):
                field_list.append(sub)
            elif isinstance(sub, And):
                field_list.extend(sub.conditions)
            else:
                or_list.append(sub.conditions)
        if not or_list:
            return And(field_list)
        # all field_list as an Or with only one node
        or_list.append([And(field_list)])
        or_cond = Or()
        for ands in product(*or_list):
            or_cond.add(And(ands))
        return or_cond

    def to_pyarrow_filter(self):
        """
        Generates filters that can be passed to ``pyarrow.parquet.ParquetDataset`` or ``pandas.read_parquet``
        in order to read only the selected partitions, thereby increase efficiency.
        Please note that the field conditions not matching a partition key will be
        ignored, so you should follow up
        with ``condition.query(df)`` to filter out unnecessary rows.

        See also `usage examples <usage.html#pyarrow-partition-filtering>`_.
        """
        if self.empty():
            return None
        cond = self.normalize()
        return cond._to_pyarrow_filter()

    def add_date_condition(
        self,
        date_field: Field,
        from_date: datetime = None,
        to_date: datetime = None,
        to_exclusive=False,
    ):
        """
        Adds to this condition that the date field should be between the passed in date range.
        This is a convenient method for working with time series.

        :param date_field: the date field
        :param from_date: if not None, the date field must be greater than or equal to this datetime value
        :param to_date: if not None, the date field must be less than this datetime value
        :param to_exclusive: if False, the date field can be equal to the ``to_date``
        """
        result = And([self])
        if from_date:
            result &= date_field >= pd.to_datetime(from_date)
        if to_date:
            if to_exclusive:
                result &= date_field < pd.to_datetime(to_date)
            else:
                result &= date_field <= pd.to_datetime(to_date)

        return result

    def add_daterange_overlap_condition(
        self,
        from_date_field: Field = None,
        to_date_field: Field = None,
        from_date: datetime = None,
        to_date: datetime = None,
        to_exclusive=False,
    ):
        """
        Adds to this condition that the two date fields must overlap with the passed in date range.
        This is a convenient method for working with time series.

        :param from_date_field: the from date field
        :param to_date_field: the to date field
        :param from_date: if not None, the ``to_date_field`` must be greater than or equal to this datetime value
        :param to_date: if not None, the ``from_date_field`` must be less than this datetime value
        :param to_exclusive: if False, the ``from_date_field`` can be equal to the ``to_date``
        """
        result = And([self])
        if from_date:
            if not to_date_field:
                raise ValueError("Need to_date_field when from_date != None")
            result &= to_date_field >= pd.to_datetime(from_date)
        if to_date:
            if not from_date_field:
                raise ValueError("Need from_date_field when to_date != None")
            if to_exclusive:
                result &= from_date_field < pd.to_datetime(to_date)
            else:
                result &= from_date_field <= pd.to_datetime(to_date)

        return result

    @abstractmethod
    def _visualize(self, id_dict, digraph, parent=None):
        raise NotImplemented()

    def _add_to_digraph(
        self, id_dict, digraph, label, color, shape=None, parent=None
    ) -> bool:
        if not self in id_dict:
            id = next(global_id)
            id_dict[self] = id
            digraph.node(
                id,
                label=label,
                style="rounded, filled",
                color=color,
                fontname="helvetica",
                shape=shape,
            )
            new_node = True
        else:
            id = id_dict[self]
            new_node = False
        if parent:
            digraph.edge(parent, id)

        return new_node

    def visualize(self, filename=None, view: bool = False):
        """
        Visualizes this condition structure with a 'png' image.
        This method requires ``graphviz`` package available.

        :param filename: the path to output the 'png' file.
        :param view: if True, show the picture
        """
        try:
            from graphviz import Digraph

            digraph = Digraph("Condition", format="png")
        except:
            raise NotImplementedError(
                "visualize() method needs graphviz package. Please install it first."
            )
        id_dict = {}
        self._visualize(id_dict, digraph)
        if filename or view:
            digraph.render(filename, view=view)


class FieldCondition(Condition):
    def __init__(self, field: Field, op: Operator, val: Any):
        """
        A condition which compares a field with a value or tests if a field in/not in a set of values.
        """
        super().__init__()
        self.field = field
        self.op = op
        self.val = val
        if (
            op not in (Operator.IN, Operator.NOT_IN)
            and not isinstance(val, str)
            and (isinstance(val, Collection))
        ):
            raise ValueError("Op '%s' not supported with a collection value", op)

    def _query_val(self):
        """
        Formats the val for sql query.
        """

        def _val(val):
            if isinstance(val, str):
                return "'" + val + "'"
            elif isinstance(val, datetime):
                return "'" + str(val) + "'"
            elif isinstance(val, Iterable):
                return "(" + ",".join([_val(v) for v in val]) + ")"
            else:
                return str(val)

        return _val(self.val)

    def to_sql_where_condition(self, db_map: Dict[str, str] = None, indent: int = 1):
        field = (
            db_map[self.field.name]
            if db_map and self.field.name in db_map
            else self.field.name
        )
        val = self._query_val()
        op = self.op.value
        if op == "==":
            op = "="
        return f"{field} {op} {val}"

    def to_df_query(self):
        field = self.field.name
        val = self._query_val()
        op = self.op.value
        if op == "=":
            op = "=="
        return f"({field} {op} {val})"

    def _to_pyarrow_filter(self):
        def _val(v):
            # convert datetime to a pd.Timestamp. Otherwise, pyarrow may throw
            # an error.
            return pd.to_datetime(v) if isinstance(v, datetime) else v

        if not isinstance(self.val, str) and isinstance(self.val, Iterable):
            val = {_val(v) for v in self.val}
        else:
            val = _val(self.val)
        return (self.field.name, self.op.value, val)

    def to_pyarrow_filter(self):
        return [self._to_pyarrow_filter()]

    def eval(self, record_dict: Dict, type_conversion: bool = False) -> bool:
        f, op, op_val = self.field.name, self.op, self.val
        if f not in record_dict:
            return True
        data = record_dict[f]
        if type_conversion:
            op_type = type(op_val)
            if op in {Operator.IN, Operator.NOT_IN}:
                op_type = type(next(iter(op_val)))
            data = op_type(data)

        if op == Operator.EQ:
            return data == op_val
        if op == Operator.NEQ:
            return data != op_val
        if op == Operator.GE:
            return data >= op_val
        if op == Operator.GT:
            return data > op_val
        if op == Operator.LE:
            return data <= op_val
        if op == Operator.LT:
            return data < op_val
        if op == Operator.IN:
            return data in op_val
        if op == Operator.NOT_IN:
            return data not in op_val

        raise NotImplementedError(f"op: {op.value} Not possible to reach here")

    def _visualize(self, id_dict, digraph, parent=None):
        self._add_to_digraph(
            id_dict,
            digraph,
            label=self.to_sql_where_condition(),
            color=FIELD_COND_COLOR,
            shape="box",
            parent=parent,
        )

    def __repr__(self) -> str:
        return f"{self.field} {self.op.value} {self._query_val()}"


class CompositeCondition(Condition, ABC):
    def __init__(self, conditions: List[Condition] = None):
        super().__init__()
        # it is best to use a set instead of a list.
        # however, the unit tests are hard to make assertion with a set.
        self.conditions: OrderedSet[Condition] = OrderedSet()
        if conditions:
            for c in conditions:
                self.add(c)

    def empty(self):
        return len(self.conditions) == 0

    def add(self, condition: Condition):
        """Adds a sub condition to this composite condition"""
        if not isinstance(condition, Condition):
            raise ValueError(
                f"Expect a Condition object. Got a {type(condition)}. "
                'You may need to enclose the condition in "()".'
            )
        if isinstance(condition, CompositeCondition):
            condition._assert_no_cycle(self)

        if isinstance(condition, type(self)):  # flatten it.
            for c in condition.conditions:
                self.conditions.add(c)
        else:
            self.conditions.add(condition)

    def _assert_no_cycle(self, check_node):
        """
        Raises error if there is a cycle.
        """
        visited = set()

        def dfs(node):
            if isinstance(node, FieldCondition):
                return
            if node == check_node:
                raise ValueError(f"Cycle detected.")
            visited.add(node)

            for c in node.conditions:
                if c not in visited:
                    dfs(c)

        dfs(self)

    def _to_sql_where_condition_common(
        self, op_str: str, db_map: Dict[str, str] = None, indent: int = 1
    ) -> str:
        indents = "\n" + "\t" * indent
        if self.empty():
            return indents + "1=1"
        sep = indents + op_str + " "
        return (
            indents
            + "("
            + sep.join(
                [p.to_sql_where_condition(db_map, indent + 1) for p in self.conditions]
            )
            + ")"
        )

    def __repr__(self) -> str:
        return self.to_sql_where_condition()

    def _visualize_composite(self, id_dict, color, label, digraph, parent=None):
        new_node = self._add_to_digraph(
            id_dict, digraph, label=label, color=color, parent=parent
        )
        if new_node:
            id = id_dict[self]
            for sub in self.conditions:
                sub._visualize(id_dict, digraph, id)


class And(CompositeCondition):
    """
    An 'and' condition composed of a list of sub conditions.
    Usage examples:

        >>> fl = FieldList(['f1', 'f2', 'f3'])
        >>> condition = And ([
        ...            fl.f1 <= 300,
        ...            fl.f2 > pd.to_datetime('20000101'),
        ...            fl.f3 == (['val1', 'val2'])
        ...         ])

    Alternatively, it can be created as follows:

        >>> condition2 = (fl.f1 <= 300) & (fl.f2 > pd.to_datetime('20000101')) & (fl.f3 == (['val1', 'val2']))
    """

    def to_sql_where_condition(
        self, db_map: Dict[str, str] = None, indent: int = 1
    ) -> str:
        return self._to_sql_where_condition_common("and", db_map, indent)

    def to_df_query(self) -> str:
        # TODO: handle empty condition
        if self.empty():
            return None  # there is no way to return a valid value here.
        return "(" + "&".join([sub.to_df_query() for sub in self.conditions]) + ")"

    def eval(self, record_dict: Dict, type_conversion: bool = False) -> bool:
        return all([sub.eval(record_dict, type_conversion) for sub in self.conditions])

    def _to_pyarrow_filter(self):
        return [sub._to_pyarrow_filter() for sub in self.conditions]

    def _visualize(self, id_dict, digraph, parent=None):
        self._visualize_composite(id_dict, AND_COLOR, "And", digraph, parent)


class Or(CompositeCondition):
    """
    An 'or' condition composed of a list of sub conditions.
    Usage examples:

        >>> fl = FieldList(['f1', 'f2', 'f3'])
        >>> condition = Or([fl.f1 <= 300,
        ...     fl.f2 > pd.to_datetime('20000101'),
        ...     fl.f3 == (['val1', 'val2'])])
        >>> condition2 = ((fl.f1 <= 300)
        ...     | (fl.f2 > pd.to_datetime('20000101'))
        ...     | (fl.f3 == (['val1', 'val2'])))
    """

    def to_sql_where_condition(
        self, db_map: Dict[str, str] = None, indent: int = 1
    ) -> str:
        return self._to_sql_where_condition_common("or", db_map, indent)

    def to_df_query(self) -> str:
        return "(" + "|".join([sub.to_df_query() for sub in self.conditions]) + ")"

    def eval(self, record_dict: Dict, type_conversion: bool = False) -> bool:
        return any([sub.eval(record_dict, type_conversion) for sub in self.conditions])

    def _to_pyarrow_filter(self):
        return [sub.to_pyarrow_filter() for sub in self.conditions]

    def _visualize(self, id_dict, digraph, parent=None):
        self._visualize_composite(id_dict, OR_COLOR, "Or", digraph, parent)


def get_test_df() -> pd.DataFrame:
    """Generates a dataframe for testing."""
    col_A = [f"a{i + 1}" for i in range(5)]
    col_B = [f"b{i + 1}" for i in range(5)]
    col_C = [f"c{i + 1}" for i in range(5)]
    dr = pd.date_range("2000-01-01", "2000-03-31")
    index = pd.MultiIndex.from_product(
        [dr, col_A, col_B, col_C], names="date A B C".split()
    )
    df = pd.DataFrame(
        data=np.random.randn(index.shape[0], 1), index=index, columns=["value"]
    )
    return df
