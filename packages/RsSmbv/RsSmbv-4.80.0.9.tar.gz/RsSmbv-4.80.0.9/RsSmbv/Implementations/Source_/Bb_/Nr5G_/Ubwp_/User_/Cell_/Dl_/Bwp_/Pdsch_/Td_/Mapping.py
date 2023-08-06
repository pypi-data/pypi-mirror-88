from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mapping:
	"""Mapping commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mapping", core, parent)

	def set(self, mapping_type: enums.MappingType, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, pdschTdoAlloc=repcap.PdschTdoAlloc.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:TD<GRP>:MAPPing \n
		Sets the DMRS-mapping type A and B. \n
			:param mapping_type: A| B
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param pdschTdoAlloc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')"""
		param = Conversions.enum_scalar_to_str(mapping_type, enums.MappingType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		pdschTdoAlloc_cmd_val = self._base.get_repcap_cmd_value(pdschTdoAlloc, repcap.PdschTdoAlloc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:TD{pdschTdoAlloc_cmd_val}:MAPPing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, pdschTdoAlloc=repcap.PdschTdoAlloc.Default) -> enums.MappingType:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:TD<GRP>:MAPPing \n
		Sets the DMRS-mapping type A and B. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param pdschTdoAlloc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
			:return: mapping_type: A| B"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		pdschTdoAlloc_cmd_val = self._base.get_repcap_cmd_value(pdschTdoAlloc, repcap.PdschTdoAlloc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:TD{pdschTdoAlloc_cmd_val}:MAPPing?')
		return Conversions.str_to_scalar_enum(response, enums.MappingType)
