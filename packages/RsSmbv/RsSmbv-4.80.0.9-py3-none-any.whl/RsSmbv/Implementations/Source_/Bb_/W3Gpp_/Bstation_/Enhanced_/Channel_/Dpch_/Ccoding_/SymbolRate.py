from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.SymbRate:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:CCODing:SRATe \n
		The command queries the symbol rate. The symbol rate depends on the selected slot format (method RsSmbv.Source.Bb.W3Gpp.
		Bstation.Enhanced.Channel.Dpch.Ccoding.Sformat.set) , and if the slot format changes, this changes automatically as well. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: srate: D7K5| D15K| D30K| D60K| D120k| D240k| D480k| D960k| D1920k| D2880k| D3840k| D4800k| D5760k| D2X1920K| D2X960K2X1920K"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:CCODing:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.SymbRate)
