from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcycle:
	"""Dcycle commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcycle", core, parent)

	def set(self, dcycle: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:LFOutput<CH>:SHAPe:PULSe:DCYCle \n
		Sets the duty cycle for the shape pulse. \n
			:param dcycle: float Range: 1E-6 to 100, Unit: PCT
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.decimal_value_to_str(dcycle)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe:PULSe:DCYCle {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:LFOutput<CH>:SHAPe:PULSe:DCYCle \n
		Sets the duty cycle for the shape pulse. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: dcycle: float Range: 1E-6 to 100, Unit: PCT"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe:PULSe:DCYCle?')
		return Conversions.str_to_float(response)
