from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dfreq:
	"""Dfreq commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dfreq", core, parent)

	def set(self, delta_freq: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:DFReq \n
		Sets the frequency offset between the NB-IoT carrier and the LTE center frequency. \n
			:param delta_freq: float Range: -10000000 to 10000000, Unit: MHz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(delta_freq)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:DFReq {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:DFReq \n
		Sets the frequency offset between the NB-IoT carrier and the LTE center frequency. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: delta_freq: float Range: -10000000 to 10000000, Unit: MHz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:DFReq?')
		return Conversions.str_to_float(response)
