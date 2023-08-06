from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, data: enums.EutraDlDataSourceUser, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:DATA \n
		Sets the data source for the selected allocation. For allocations with two codewords, the data source for the second
		codeword is automatically set to the data source set for the first one. \n
			:param data: USER1| USER2| USER3| USER4| PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE| MIB| MCCH| MTCH MIB (Result parameter) Indicates that the PBCH transmits real MIB data. (See also method RsSmbv.Source.Bb.Eutra.Dl.Pbch.mib) MCCH|MTCH (Result parameter) Indicates allocations in the MBSFN subframes, if MBSFN is used. (See also method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.mode)
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')"""
		param = Conversions.enum_scalar_to_str(data, enums.EutraDlDataSourceUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> enums.EutraDlDataSourceUser:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:DATA \n
		Sets the data source for the selected allocation. For allocations with two codewords, the data source for the second
		codeword is automatically set to the data source set for the first one. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: data: USER1| USER2| USER3| USER4| PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE| MIB| MCCH| MTCH MIB (Result parameter) Indicates that the PBCH transmits real MIB data. (See also method RsSmbv.Source.Bb.Eutra.Dl.Pbch.mib) MCCH|MTCH (Result parameter) Indicates allocations in the MBSFN subframes, if MBSFN is used. (See also method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.mode)"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDlDataSourceUser)
