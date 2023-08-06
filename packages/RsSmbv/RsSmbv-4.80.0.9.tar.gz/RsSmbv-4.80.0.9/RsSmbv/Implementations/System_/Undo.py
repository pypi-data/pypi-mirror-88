from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Undo:
	"""Undo commands group definition. 5 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("undo", core, parent)

	def clone(self) -> 'Undo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Undo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def hclear(self):
		"""hclear commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hclear'):
			from .Undo_.Hclear import Hclear
			self._hclear = Hclear(self._core, self._base)
		return self._hclear

	@property
	def hid(self):
		"""hid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hid'):
			from .Undo_.Hid import Hid
			self._hid = Hid(self._core, self._base)
		return self._hid

	@property
	def hlable(self):
		"""hlable commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_hlable'):
			from .Undo_.Hlable import Hlable
			self._hlable = Hlable(self._core, self._base)
		return self._hlable

	def get_state(self) -> bool:
		"""SYSTem:UNDO:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:UNDO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SYSTem:UNDO:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:UNDO:STATe {param}')
