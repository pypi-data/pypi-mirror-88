from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def set(self, length: enums.NumbersH, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, pdschTdoAlloc=repcap.PdschTdoAlloc.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:TD<GRP>:LENGth \n
		Sets the PDSCH allocation length. \n
			:param length: 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param pdschTdoAlloc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')"""
		param = Conversions.enum_scalar_to_str(length, enums.NumbersH)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		pdschTdoAlloc_cmd_val = self._base.get_repcap_cmd_value(pdschTdoAlloc, repcap.PdschTdoAlloc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:TD{pdschTdoAlloc_cmd_val}:LENGth {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, pdschTdoAlloc=repcap.PdschTdoAlloc.Default) -> enums.NumbersH:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:TD<GRP>:LENGth \n
		Sets the PDSCH allocation length. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param pdschTdoAlloc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
			:return: length: 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		pdschTdoAlloc_cmd_val = self._base.get_repcap_cmd_value(pdschTdoAlloc, repcap.PdschTdoAlloc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:TD{pdschTdoAlloc_cmd_val}:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersH)
