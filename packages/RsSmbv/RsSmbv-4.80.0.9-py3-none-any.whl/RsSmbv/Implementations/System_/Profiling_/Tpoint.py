from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tpoint:
	"""Tpoint commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpoint", core, parent)

	def clone(self) -> 'Tpoint':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tpoint(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Tpoint_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def get_restart(self) -> List[str]:
		"""SYSTem:PROFiling:TPOint:RESTart \n
		No command help available \n
			:return: module_and_tp: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:TPOint:RESTart?')
		return Conversions.str_to_str_list(response)

	def set_restart(self, module_and_tp: List[str]) -> None:
		"""SYSTem:PROFiling:TPOint:RESTart \n
		No command help available \n
			:param module_and_tp: No help available
		"""
		param = Conversions.list_to_csv_quoted_str(module_and_tp)
		self._core.io.write(f'SYSTem:PROFiling:TPOint:RESTart {param}')
