from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ai:
	"""Ai commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ai", core, parent)

	def clone(self) -> 'Ai':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ai(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Ai_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, ai: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:[NMESsage]:[INAV]:IONospheric:AI<CH> \n
		Sets the parameters effective ionization level 1st to 3rd order of the satellite's navigation message. \n
			:param ai: integer Range: a_i0 (0 to 2047) , a_i1 (-1024 to 1023) , a_i2 (-8192 to 8191)
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(ai)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:INAV:IONospheric:AI{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:[NMESsage]:[INAV]:IONospheric:AI<CH> \n
		Sets the parameters effective ionization level 1st to 3rd order of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: ai: integer Range: a_i0 (0 to 2047) , a_i1 (-1024 to 1023) , a_i2 (-8192 to 8191)"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:INAV:IONospheric:AI{channel_cmd_val}?')
		return Conversions.str_to_int(response)
