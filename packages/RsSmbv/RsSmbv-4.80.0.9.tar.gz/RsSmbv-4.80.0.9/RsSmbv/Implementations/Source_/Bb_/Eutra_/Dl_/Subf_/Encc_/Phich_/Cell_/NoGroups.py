from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NoGroups:
	"""NoGroups commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("noGroups", core, parent)

	def set(self, group_count: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Nr1) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:[CELL<CCIDX>]:NOGRoups \n
		Queries the number of available PHICH groups. \n
			:param group_count: integer Range: 0 to dynamic
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.decimal_value_to_str(group_count)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:CELL{carrierComponent_cmd_val}:NOGRoups {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Nr1) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:[CELL<CCIDX>]:NOGRoups \n
		Queries the number of available PHICH groups. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:return: group_count: integer Range: 0 to dynamic"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:CELL{carrierComponent_cmd_val}:NOGRoups?')
		return Conversions.str_to_int(response)
