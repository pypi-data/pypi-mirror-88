from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def external(self):
		"""external commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_external'):
			from .Trigger_.External import External
			self._external = External(self._core, self._base)
		return self._external

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PulsTrigModeWithSingle:
		"""[SOURce<HW>]:PULM:TRIGger:MODE \n
		Selects a trigger mode - auto, single, external, external single or external gated - for generating the modulation signal. \n
			:return: mode: AUTO| EXTernal| EGATe| SINGle| ESINgle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRIGger:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PulsTrigModeWithSingle)

	def set_mode(self, mode: enums.PulsTrigModeWithSingle) -> None:
		"""[SOURce<HW>]:PULM:TRIGger:MODE \n
		Selects a trigger mode - auto, single, external, external single or external gated - for generating the modulation signal. \n
			:param mode: AUTO| EXTernal| EGATe| SINGle| ESINgle
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PulsTrigModeWithSingle)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRIGger:MODE {param}')
