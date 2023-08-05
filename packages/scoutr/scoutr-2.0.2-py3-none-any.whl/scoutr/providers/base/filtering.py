import json
import re
from abc import abstractmethod
from decimal import Decimal
from typing import Any, Optional, List, Dict, Tuple, Callable, Set
from urllib.parse import unquote_plus

from scoutr.exceptions import BadRequestException
from scoutr.models.user import FilterField, User


class Filtering:

    OPERATION_EQUAL = 'eq'
    OPERATION_NOT_EQUAL = 'ne'
    OPERATION_STARTS_WITH = 'startswith'
    OPERATION_CONTAINS = 'contains'
    OPERATION_NOT_CONTAINS = 'notcontains'
    OPERATION_EXISTS = 'exists'
    OPERATION_GREATER_THAN = 'gt'
    OPERATION_LESS_THAN = 'lt'
    OPERATION_GREATER_THAN_EQUAL = 'ge'
    OPERATION_LESS_THAN_EQUAL = 'le'
    OPERATION_BETWEEN = 'between'
    OPERATION_IN = 'in'
    OPERATION_NOT_IN = 'notin'

    FILTER_ACTION_READ = 'READ'
    FILTER_ACTION_CREATE = 'CREATE'
    FILTER_ACTION_UPDATE = 'UPDATE'
    FILTER_ACTION_DELETE = 'DELETE'

    NUMERIC_OPERATIONS = (
        OPERATION_GREATER_THAN,
        OPERATION_LESS_THAN,
        OPERATION_GREATER_THAN_EQUAL,
        OPERATION_LESS_THAN_EQUAL,
    )

    @property
    def operations(self) -> Dict[str, Callable[[str, Any], Any]]:
        """
        List of supported operations

        :return: Supported operations
        :rtype: dict
        """
        return {
            self.OPERATION_EQUAL: self.equals,
            self.OPERATION_NOT_EQUAL: self.not_equal,
            self.OPERATION_CONTAINS: self.contains,
            self.OPERATION_NOT_CONTAINS: self.not_contains,
            self.OPERATION_STARTS_WITH: self.starts_with,
            self.OPERATION_EXISTS: self.exists,
            self.OPERATION_GREATER_THAN: self.greater_than,
            self.OPERATION_LESS_THAN: self.less_than,
            self.OPERATION_GREATER_THAN_EQUAL: self.greater_than_equal,
            self.OPERATION_LESS_THAN_EQUAL: self.less_than_equal,
            self.OPERATION_BETWEEN: self.between,
            self.OPERATION_IN: self.is_in,
            self.OPERATION_NOT_IN: self.not_in
        }

    @abstractmethod
    def And(self, condition1, condition2):
        raise NotImplementedError

    @abstractmethod
    def Or(self, condition1, condition2):
        raise NotImplementedError

    @abstractmethod
    def equals(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def not_equal(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def starts_with(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def contains(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def not_contains(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def exists(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def greater_than(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def less_than(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def greater_than_equal(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def less_than_equal(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def between(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def is_in(self, attr: str, value):
        raise NotImplementedError

    @abstractmethod
    def not_in(self, attr: str, value):
        raise NotImplementedError

    def _user_filters(self, filter_fields: List[FilterField]) -> Any:
        # Merge all possible values for this filter key together
        filters: Dict[str, List[FilterField]] = {}
        for filter_field in filter_fields:
            filters.setdefault(filter_field.field, list())
            filters[filter_field.field].append(filter_field)

        # Perform the filter
        conditions = None
        for key, filter_items in filters.items():
            if len(filter_items) == 1:
                # Perform a single query
                item = filter_items[0]
                conditions = self.perform_filter(conditions, f'{key}__{item.operator}', item.value)
            elif len(filter_items) > 1:
                # Perform an OR query against all possible values for this key
                filter_conds = None
                for item in filter_items:
                    filter_conds = self.Or(
                        filter_conds,
                        self.perform_filter(None, f'{key}__{item.operator}', item.value)
                    )
                conditions = self.And(conditions, filter_conds)

        return conditions

    def filter(self, user: Optional[User], filters: Optional[dict] = None, action: str = FILTER_ACTION_READ) -> Any:
        conditions = None
        if filters is None:
            filters = {}

        if user:
            # Select filter type (defaults to read filters)
            if action == self.FILTER_ACTION_CREATE:
                filter_fields = user.create_filters
            elif action == self.FILTER_ACTION_UPDATE:
                filter_fields = user.update_filters
            elif action == self.FILTER_ACTION_DELETE:
                filter_fields = user.delete_filters
            else:
                filter_fields = user.read_filters

            # Perform user filter
            conditions = self._user_filters(filter_fields)

        # Run filter operation
        return self._filter(conditions, filters)

    def _filter(self, conditions: Any, filters: dict) -> Any:
        # Build filters that were passed in
        for key, value in filters.items():
            if isinstance(value, list):
                # Multi-value filter
                for item in value:
                    if not isinstance(item, str):
                        raise BadRequestException('Query filter value must be a string or list of strings')
                    conditions = self.perform_filter(conditions, key, item)
            elif isinstance(value, str):
                # Single value filter
                conditions = self.perform_filter(conditions, key, value)
            else:
                # Invalid
                raise BadRequestException('Query filter value must be a string or list of strings')

        return conditions

    def get_operator(self, key: str) -> Tuple[str, str]:
        # Check if this is a magic operator
        operation = self.OPERATION_EQUAL
        magic_operator_match = re.match('^(.+)__(.+)$', key)
        if magic_operator_match:
            key = magic_operator_match.group(1)
            operation = magic_operator_match.group(2)

        # Fetch condition function from operation map
        return key, operation

    def perform_filter(self, conditions: Any, key: str, value: Any) -> Any:
        # Unquote the value
        if isinstance(value, str):
            value = unquote_plus(value)
            if value == '':
                raise BadRequestException('Filter key %s has no value' % key)

        # Get operator
        key, operator = self.get_operator(key)

        # Convert to decimal if this is a numeric operation
        if isinstance(value, str) and value.isnumeric() and operator in self.NUMERIC_OPERATIONS:
            value = Decimal(value)

        # Perform the filter operation
        func = self.operations.get(operator)
        try:
            # Check if this is an unknown operation
            if func is None:
                raise NotImplementedError

            # Run the condition function
            condition = func(key, value)

            # If condition is null, do not apply the condition
            if condition is not None:
                return self.And(conditions, condition)
        except NotImplementedError:
            raise BadRequestException(f"Provider does not support magic operator '{operator}")

        return conditions

    def multi_filter(self, user, filter_key, value):
        # Make sure a value was provided
        if not value:
            raise BadRequestException('No search values were provided')

        # Build pre-set filters
        base_condition = self.filter(user)

        # Build the multi-filters
        expressions = []

        if isinstance(value, list):
            if len(value) < 99:
                condition = self.And(base_condition, self.is_in(filter_key, value))
                expressions.append(condition)
            else:
                for i in range(0, len(value), 99):
                    condition = self.And(base_condition, self.is_in(filter_key, value[i:i + 99]))
                    expressions.append(condition)
        else:
            condition = self.And(base_condition, self.equals(filter_key, value))
            expressions.append(condition)

        return expressions


class LocalFiltering(Filtering):
    def __init__(self, data: dict):
        self.data = data
        self.failed_filters: Set[str] = set()

    def _user_filters(self, filter_fields: List[FilterField]) -> Any:
        # Merge all possible values for this filter key together
        filters: Dict[str, List[FilterField]] = {}
        for filter_field in filter_fields:
            filters.setdefault(filter_field.field, list())
            filters[filter_field.field].append(filter_field)

        # Perform the filter
        conditions = None
        for key, filter_items in filters.items():
            if len(filter_items) == 1:
                # Perform a single query
                item = filter_items[0]
                existing_conditions = conditions
                conditions = self.perform_filter(conditions, f'{key}__{item.operator}', item.value)
                if (existing_conditions is None or existing_conditions is True) and conditions is False:
                    self.failed_filters.add(key)
            elif len(filter_items) > 1:
                # Perform an OR query against all possible values for this key
                filter_conds = None
                for item in filter_items:
                    filter_conds = self.Or(
                        filter_conds,
                        self.perform_filter(None, f'{key}__{item.operator}', item.value)
                    )
                existing_conditions = conditions
                conditions = self.And(conditions, filter_conds)
                if (existing_conditions is None or existing_conditions is True) and conditions is False:
                    self.failed_filters.add(key)

        return conditions

    def And(self, condition1, condition2):
        if condition1 is None:
            condition1 = True
        if condition2 is None:
            condition2 = True

        return condition1 and condition2

    def Or(self, condition1, condition2):
        if condition1 is None:
            condition1 = True
        if condition2 is None:
            condition2 = True

        return condition1 or condition2

    def equals(self, attr: str, value):
        if attr not in self.data:
            return False
        return self.data[attr] == value

    def not_equal(self, attr: str, value):
        if attr not in self.data:
            return False
        return self.data[attr] != value

    def contains(self, attr: str, value: str):
        if attr not in self.data:
            return False
        return value in self.data[attr]

    def not_contains(self, attr: str, value: str):
        if attr not in self.data:
            return False
        return value not in self.data[attr]

    def starts_with(self, attr: str, value: str):
        if attr not in self.data:
            return False
        return self.data[attr].startswith(value)

    def exists(self, attr: str, value):
        if value == 'true':
            return attr in self.data
        elif value == 'false':
            return attr not in self.data
        else:
            raise Exception('Invalid value for exists operation')

    def greater_than(self, attr: str, value):
        if attr not in self.data:
            return False
        return self.data[attr] > value

    def less_than(self, attr: str, value):
        if attr not in self.data:
            return False
        return self.data[attr] < value

    def greater_than_equal(self, attr: str, value):
        if attr not in self.data:
            return False
        return self.data[attr] >= value

    def less_than_equal(self, attr: str, value):
        if attr not in self.data:
            return False
        return self.data[attr] <= value

    def between(self, attr: str, value):
        if attr not in self.data:
            return False
        if isinstance(value, list):
            values = value
        else:
            values = json.loads(value)
        if not len(values) == 2:
            raise Exception('Between operation requires two values')
        return values[0] <= self.data[attr] <= values[1]

    def is_in(self, attr: str, value):
        if attr not in self.data:
            return False
        if isinstance(value, list):
            values = value
        else:
            values = json.loads(value)
        return self.data[attr] in values

    def not_in(self, attr: str, value):
        if attr not in self.data:
            return False
        if isinstance(value, list):
            values = value
        else:
            values = json.loads(value)
        return self.data[attr] not in values
