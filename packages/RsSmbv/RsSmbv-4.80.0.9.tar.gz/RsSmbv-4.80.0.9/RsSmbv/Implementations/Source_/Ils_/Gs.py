from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gs:
	"""Gs commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gs", core, parent)

	def clone(self) -> 'Gs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ddm(self):
		"""ddm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ddm'):
			from .Gs_.Ddm import Ddm
			self._ddm = Ddm(self._core, self._base)
		return self._ddm

	def preset(self) -> None:
		"""[SOURce<HW>]:ILS:GS:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:ILS:GS:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:GS:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:ILS:GS:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:ILS:GS:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:STATe {param}')
