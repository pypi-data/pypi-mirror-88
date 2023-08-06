from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cchannel:
	"""Cchannel commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cchannel", core, parent)

	def clone(self) -> 'Cchannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cchannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def revision(self):
		"""revision commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_revision'):
			from .Cchannel_.Revision import Revision
			self._revision = Revision(self._core, self._base)
		return self._revision

	def get_psoffset(self) -> int:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:CCHannel:PSOFfset \n
		Sets the offset (in slots) from the start of control channel cycle to the start of the synchronous message capsule that
		contains the Sync Message. \n
			:return: ps_offset: integer Range: 0 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:CCHannel:PSOFfset?')
		return Conversions.str_to_int(response)

	def set_psoffset(self, ps_offset: int) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:CCHannel:PSOFfset \n
		Sets the offset (in slots) from the start of control channel cycle to the start of the synchronous message capsule that
		contains the Sync Message. \n
			:param ps_offset: integer Range: 0 to 3
		"""
		param = Conversions.decimal_value_to_str(ps_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:CCHannel:PSOFfset {param}')

	# noinspection PyTypeChecker
	def get_rate(self) -> enums.EvdoDataRate:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:CCHannel:RATE \n
		Sets the rate that the control channel messages are transmitted at. \n
			:return: rate: DR4K8| DR9K6| DR19K2| DR38K4| DR76K8| DR153K6| DR307K2| DR614K4| DR921K6| DR1228K8| DR1536K| DR1843K2| DR2457K6| DR3072K| DR460K8| DR768K| DR1075K2| DR2150K4| DR3686K4| DR4300K8| DR4915K2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:CCHannel:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoDataRate)

	def set_rate(self, rate: enums.EvdoDataRate) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:CCHannel:RATE \n
		Sets the rate that the control channel messages are transmitted at. \n
			:param rate: DR4K8| DR9K6| DR19K2| DR38K4| DR76K8| DR153K6| DR307K2| DR614K4| DR921K6| DR1228K8| DR1536K| DR1843K2| DR2457K6| DR3072K| DR460K8| DR768K| DR1075K2| DR2150K4| DR3686K4| DR4300K8| DR4915K2
		"""
		param = Conversions.enum_scalar_to_str(rate, enums.EvdoDataRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:CCHannel:RATE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:CCHannel:STATe \n
		Enables or disables the control channel messages. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:CCHannel:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:CCHannel:STATe \n
		Enables or disables the control channel messages. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:CCHannel:STATe {param}')
