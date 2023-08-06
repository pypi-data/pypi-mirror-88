from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tick:
	"""Tick commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tick", core, parent)

	def clone(self) -> 'Tick':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tick(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Tick_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	def get_value(self) -> str:
		"""SYSTem:PROFiling:TICK \n
		No command help available \n
			:return: answer: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:TICK?')
		return trim_str_response(response)
