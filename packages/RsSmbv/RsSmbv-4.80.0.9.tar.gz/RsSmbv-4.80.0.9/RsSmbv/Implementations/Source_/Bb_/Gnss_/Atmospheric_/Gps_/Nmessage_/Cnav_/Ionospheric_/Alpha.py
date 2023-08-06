from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alpha:
	"""Alpha commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alpha", core, parent)

	def clone(self) -> 'Alpha':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alpha(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Alpha_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, alpha: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:GPS:[NMESsage]:[CNAV]:IONospheric:ALPHa<CH> \n
		Sets the parameters alpha_0 to alpha_3 of the satellite's navigation message. \n
			:param alpha: integer Range: -128 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(alpha)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GPS:NMESsage:CNAV:IONospheric:ALPHa{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:GPS:[NMESsage]:[CNAV]:IONospheric:ALPHa<CH> \n
		Sets the parameters alpha_0 to alpha_3 of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: alpha: integer Range: -128 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GPS:NMESsage:CNAV:IONospheric:ALPHa{channel_cmd_val}?')
		return Conversions.str_to_int(response)
