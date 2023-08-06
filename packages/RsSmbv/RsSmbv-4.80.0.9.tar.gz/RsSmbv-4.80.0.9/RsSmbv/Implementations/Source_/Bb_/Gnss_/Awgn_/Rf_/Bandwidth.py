from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandwidth", core, parent)

	def set(self, system_band_width: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:BWIDth \n
		Sets the RF bandwidth to which the set carrier/noise ratio relates. Within this frequency range, the signal is
		superimposed with a noise signal which level corresponds exactly to the set C/N or S/N ratio. \n
			:param system_band_width: integer Range: 1E3 to 500E6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(system_band_width)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:BWIDth {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:BWIDth \n
		Sets the RF bandwidth to which the set carrier/noise ratio relates. Within this frequency range, the signal is
		superimposed with a noise signal which level corresponds exactly to the set C/N or S/N ratio. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: system_band_width: integer Range: 1E3 to 500E6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:BWIDth?')
		return Conversions.str_to_int(response)
