from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NaPort:
	"""NaPort commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("naPort", core, parent)

	def set(self, num_aps: enums.NumberOfPorts, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:NAPort \n
		Sets the number of antenna ports for PUSCH transmission. Use the command BB:EUTRa:ALLoc<ch0>:PUSCh:PRECoding:NAPused to
		query the number of used antenna ports. \n
			:param num_aps: AP1 | AP2 | AP4
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(num_aps, enums.NumberOfPorts)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:NAPort {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> enums.NumberOfPorts:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:NAPort \n
		Sets the number of antenna ports for PUSCH transmission. Use the command BB:EUTRa:ALLoc<ch0>:PUSCh:PRECoding:NAPused to
		query the number of used antenna ports. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: num_aps: AP1 | AP2 | AP4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:NAPort?')
		return Conversions.str_to_scalar_enum(response, enums.NumberOfPorts)
