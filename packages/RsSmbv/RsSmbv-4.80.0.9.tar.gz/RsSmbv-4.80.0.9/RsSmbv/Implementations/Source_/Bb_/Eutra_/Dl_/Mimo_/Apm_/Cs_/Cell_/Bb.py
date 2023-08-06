from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bb:
	"""Bb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bb", core, parent)

	def set(self, ant_port_cc_index: enums.EutraCcIndex, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:APM:CS:CELL:BB<ST> \n
		Maps a component carrier to a baseband. \n
			:param ant_port_cc_index: PC| SC1| SC2| SC3| SC4 Component carrier
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(ant_port_cc_index, enums.EutraCcIndex)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:APM:CS:CELL:BB{stream_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraCcIndex:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:APM:CS:CELL:BB<ST> \n
		Maps a component carrier to a baseband. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: ant_port_cc_index: PC| SC1| SC2| SC3| SC4 Component carrier"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:APM:CS:CELL:BB{stream_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCcIndex)
