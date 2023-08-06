from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EvdoMarkMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param mode: SLOT| PNSPeriod| ESM| CSPeriod| USER| RATio SLOT Each slot (every 1.67 ms) PNSPeriod Every 26.67 ms (PN Sequence Period) ESM Every 2 s (even second mark) . CSPeriod Each arbitrary waveform sequence RATio Regular marker signal USER Every user-defined period.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EvdoMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EvdoMarkMode:
		"""[SOURce<HW>]:BB:EVDO:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: SLOT| PNSPeriod| ESM| CSPeriod| USER| RATio SLOT Each slot (every 1.67 ms) PNSPeriod Every 26.67 ms (PN Sequence Period) ESM Every 2 s (even second mark) . CSPeriod Each arbitrary waveform sequence RATio Regular marker signal USER Every user-defined period."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoMarkMode)
