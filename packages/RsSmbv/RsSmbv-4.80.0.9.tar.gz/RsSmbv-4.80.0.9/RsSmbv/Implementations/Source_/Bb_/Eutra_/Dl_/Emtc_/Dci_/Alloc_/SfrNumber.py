from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfrNumber:
	"""SfrNumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sfrNumber", core, parent)

	def set(self, dci_sf_rep_number: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:SFRNumber \n
		If method RsSmbv.Source.Bb.Eutra.Dl.User.Epdcch.Cell.Set.Repmpdcch.set ≥2, sets the DCI field DCI subframe repetition
		number. \n
			:param dci_sf_rep_number: integer Range: 0 to 3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(dci_sf_rep_number)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:SFRNumber {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:SFRNumber \n
		If method RsSmbv.Source.Bb.Eutra.Dl.User.Epdcch.Cell.Set.Repmpdcch.set ≥2, sets the DCI field DCI subframe repetition
		number. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: dci_sf_rep_number: integer Range: 0 to 3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:SFRNumber?')
		return Conversions.str_to_int(response)
