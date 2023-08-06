from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	def set(self, base_mod_type: enums.C5GbaseMod, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:MODulation \n
		Sets the modulation type of an allocation. \n
			:param base_mod_type: BPSK| QPSK| QAM16| QAM64| QAM256| SCMA| CIQ CIQ Custom IQ data file, loaded with the command method RsSmbv.Source.Bb.Ofdm.Alloc.Ciqfile.set.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(base_mod_type, enums.C5GbaseMod)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:MODulation {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.C5GbaseMod:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:MODulation \n
		Sets the modulation type of an allocation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: base_mod_type: BPSK| QPSK| QAM16| QAM64| QAM256| SCMA| CIQ CIQ Custom IQ data file, loaded with the command method RsSmbv.Source.Bb.Ofdm.Alloc.Ciqfile.set."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.C5GbaseMod)
