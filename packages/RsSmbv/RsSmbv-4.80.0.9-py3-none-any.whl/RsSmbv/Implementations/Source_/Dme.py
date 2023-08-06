from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dme:
	"""Dme commands group definition. 12 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dme", core, parent)

	def clone(self) -> 'Dme':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dme(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def analysis(self):
		"""analysis commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_analysis'):
			from .Dme_.Analysis import Analysis
			self._analysis = Analysis(self._core, self._base)
		return self._analysis

	def get_low_emission(self) -> bool:
		"""[SOURce<HW>]:DME:LOWemission \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:LOWemission?')
		return Conversions.str_to_bool(response)

	def set_low_emission(self, state: bool) -> None:
		"""[SOURce<HW>]:DME:LOWemission \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:LOWemission {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:DME:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:DME:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:DME:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:DME:PRESet')

	# noinspection PyTypeChecker
	def get_trigger(self) -> enums.VimDmeTrigMode:
		"""[SOURce<HW>]:DME:TRIGger \n
		No command help available \n
			:return: trigger_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:TRIGger?')
		return Conversions.str_to_scalar_enum(response, enums.VimDmeTrigMode)

	def set_trigger(self, trigger_mode: enums.VimDmeTrigMode) -> None:
		"""[SOURce<HW>]:DME:TRIGger \n
		No command help available \n
			:param trigger_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(trigger_mode, enums.VimDmeTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:DME:TRIGger {param}')
