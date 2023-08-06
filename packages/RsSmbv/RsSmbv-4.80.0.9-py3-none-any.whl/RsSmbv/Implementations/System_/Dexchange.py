from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dexchange:
	"""Dexchange commands group definition. 12 total commands, 3 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dexchange", core, parent)

	def clone(self) -> 'Dexchange':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dexchange(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Dexchange_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def template(self):
		"""template commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_template'):
			from .Dexchange_.Template import Template
			self._template = Template(self._core, self._base)
		return self._template

	@property
	def transaction(self):
		"""transaction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_transaction'):
			from .Dexchange_.Transaction import Transaction
			self._transaction = Transaction(self._core, self._base)
		return self._transaction

	def get_catalog(self) -> List[str]:
		"""SYSTem:DEXChange:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SYSTem:DEXChange:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_debug(self) -> bool:
		"""SYSTem:DEXChange:DEBug \n
		No command help available \n
			:return: debug: No help available
		"""
		response = self._core.io.query_str('SYSTem:DEXChange:DEBug?')
		return Conversions.str_to_bool(response)

	def set_debug(self, debug: bool) -> None:
		"""SYSTem:DEXChange:DEBug \n
		No command help available \n
			:param debug: No help available
		"""
		param = Conversions.bool_to_str(debug)
		self._core.io.write(f'SYSTem:DEXChange:DEBug {param}')

	def delete(self, filename: str) -> None:
		"""SYSTem:DEXChange:DELete \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SYSTem:DEXChange:DELete {param}')

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.DevExpFormat:
		"""SYSTem:DEXChange:FORMat \n
		No command help available \n
			:return: format_py: No help available
		"""
		response = self._core.io.query_str('SYSTem:DEXChange:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.DevExpFormat)

	def set_format_py(self, format_py: enums.DevExpFormat) -> None:
		"""SYSTem:DEXChange:FORMat \n
		No command help available \n
			:param format_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.DevExpFormat)
		self._core.io.write(f'SYSTem:DEXChange:FORMat {param}')

	def get_select(self) -> str:
		"""SYSTem:DEXChange:SELect \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SYSTem:DEXChange:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SYSTem:DEXChange:SELect \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SYSTem:DEXChange:SELect {param}')
