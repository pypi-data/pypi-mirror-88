from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OcqiMin:
	"""OcqiMin commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ocqiMin", core, parent)

	def set(self, chan_cod_ocqi_min: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:CCODing:OCQimin \n
		For PUSCH channel coding and multiplexing mode UCI only, sets the parameter O_CQI-Min. \n
			:param chan_cod_ocqi_min: integer Range: 1 to 472
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(chan_cod_ocqi_min)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:CCODing:OCQimin {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:CCODing:OCQimin \n
		For PUSCH channel coding and multiplexing mode UCI only, sets the parameter O_CQI-Min. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: chan_cod_ocqi_min: integer Range: 1 to 472"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:CCODing:OCQimin?')
		return Conversions.str_to_int(response)
