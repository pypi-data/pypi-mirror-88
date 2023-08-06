from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gslope:
	"""Gslope commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gslope", core, parent)

	def clone(self) -> 'Gslope':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gslope(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ddm(self):
		"""ddm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ddm'):
			from .Gslope_.Ddm import Ddm
			self._ddm = Ddm(self._core, self._base)
		return self._ddm

	def preset(self) -> None:
		"""[SOURce<HW>]:ILS:GSLope:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:GSLope:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:ILS:GSLope:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:GSLope:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:ILS:GSLope:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GSLope:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:ILS:GSLope:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GSLope:STATe {param}')
