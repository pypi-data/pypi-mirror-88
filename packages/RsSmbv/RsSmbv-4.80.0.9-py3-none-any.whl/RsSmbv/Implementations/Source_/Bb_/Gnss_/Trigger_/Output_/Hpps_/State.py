from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, high_prec_pps_stat: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:HPPS:STATe \n
		Enables generation of a high-precision PPS marker signal. \n
			:param high_prec_pps_stat: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.bool_to_str(high_prec_pps_stat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:HPPS:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:HPPS:STATe \n
		Enables generation of a high-precision PPS marker signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: high_prec_pps_stat: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:HPPS:STATe?')
		return Conversions.str_to_bool(response)
