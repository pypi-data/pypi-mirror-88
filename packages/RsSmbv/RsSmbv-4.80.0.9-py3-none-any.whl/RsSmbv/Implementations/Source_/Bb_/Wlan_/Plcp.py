from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plcp:
	"""Plcp commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plcp", core, parent)

	def clone(self) -> 'Plcp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Plcp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def lcBit(self):
		"""lcBit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcBit'):
			from .Plcp_.LcBit import LcBit
			self._lcBit = LcBit(self._core, self._base)
		return self._lcBit

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.CckFormat:
		"""[SOURce<HW>]:BB:WLAN:PLCP:FORMat \n
		No command help available \n
			:return: format_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PLCP:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.CckFormat)

	def set_format_py(self, format_py: enums.CckFormat) -> None:
		"""[SOURce<HW>]:BB:WLAN:PLCP:FORMat \n
		No command help available \n
			:param format_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.CckFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PLCP:FORMat {param}')
