from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scontrol:
	"""Scontrol commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scontrol", core, parent)

	def clone(self) -> 'Scontrol':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scontrol(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fragment(self):
		"""fragment commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fragment'):
			from .Scontrol_.Fragment import Fragment
			self._fragment = Fragment(self._core, self._base)
		return self._fragment

	@property
	def sequence(self):
		"""sequence commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sequence'):
			from .Scontrol_.Sequence import Sequence
			self._sequence = Sequence(self._core, self._base)
		return self._sequence

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MAC:SCONtrol:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:SCONtrol:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MAC:SCONtrol:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:SCONtrol:STATe {param}')
