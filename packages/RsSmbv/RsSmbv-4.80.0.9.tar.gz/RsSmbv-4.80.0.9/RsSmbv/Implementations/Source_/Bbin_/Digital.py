from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digital:
	"""Digital commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("digital", core, parent)

	def clone(self) -> 'Digital':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Digital(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def asetting(self):
		"""asetting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_asetting'):
			from .Digital_.Asetting import Asetting
			self._asetting = Asetting(self._core, self._base)
		return self._asetting

	# noinspection PyTypeChecker
	def get_interface(self) -> enums.BbinInterfaceMode:
		"""[SOURce<HW>]:BBIN:DIGital:INTerface \n
		Selects the input connector at that the signal is fed. \n
			:return: bb_in_dig_interface: DIGital| HSDin | DIGital| HSDin DIN Dig I/Q HSDin HS Dig I/Q
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:DIGital:INTerface?')
		return Conversions.str_to_scalar_enum(response, enums.BbinInterfaceMode)

	def set_interface(self, bb_in_dig_interface: enums.BbinInterfaceMode) -> None:
		"""[SOURce<HW>]:BBIN:DIGital:INTerface \n
		Selects the input connector at that the signal is fed. \n
			:param bb_in_dig_interface: DIGital| HSDin | DIGital| HSDin DIN Dig I/Q HSDin HS Dig I/Q
		"""
		param = Conversions.enum_scalar_to_str(bb_in_dig_interface, enums.BbinInterfaceMode)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:DIGital:INTerface {param}')
