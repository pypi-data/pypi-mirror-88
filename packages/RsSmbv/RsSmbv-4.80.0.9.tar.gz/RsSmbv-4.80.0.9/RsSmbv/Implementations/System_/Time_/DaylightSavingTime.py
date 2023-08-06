from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaylightSavingTime:
	"""DaylightSavingTime commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("daylightSavingTime", core, parent)

	def clone(self) -> 'DaylightSavingTime':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DaylightSavingTime(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def rule(self):
		"""rule commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rule'):
			from .DaylightSavingTime_.Rule import Rule
			self._rule = Rule(self._core, self._base)
		return self._rule

	def get_mode(self) -> str:
		"""SYSTem:TIME:DSTime:MODE \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:DSTime:MODE?')
		return trim_str_response(response)

	def set_mode(self, pseudo_string: str) -> None:
		"""SYSTem:TIME:DSTime:MODE \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:DSTime:MODE {param}')
