from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Additional:
	"""Additional commands group definition. 5 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("additional", core, parent)

	def clone(self) -> 'Additional':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Additional(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def lcMask(self):
		"""lcMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcMask'):
			from .Additional_.LcMask import LcMask
			self._lcMask = LcMask(self._core, self._base)
		return self._lcMask

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Additional_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Additional_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:COUNt \n
		Sets the number of additional mobile stations. \n
			:return: count: integer Range: 1 to 64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:COUNt \n
		Sets the number of additional mobile stations. \n
			:param count: integer Range: 1 to 64
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:COUNt {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:STATe \n
		The command activates additional mobile stations. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:STATe \n
		The command activates additional mobile stations. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:STATe {param}')
