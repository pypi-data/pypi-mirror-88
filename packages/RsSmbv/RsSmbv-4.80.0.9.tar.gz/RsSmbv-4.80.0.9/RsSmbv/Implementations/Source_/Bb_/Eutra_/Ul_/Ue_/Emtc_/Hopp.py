from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hopp:
	"""Hopp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hopp", core, parent)

	def set(self, hopping_interval: enums.EutraIotHoppingIvl, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:HOPP \n
		Sets the narrowband hopping interval. \n
			:param hopping_interval: H1| H2| H4| H5| H8| H10| H16| H20| H40
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(hopping_interval, enums.EutraIotHoppingIvl)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:HOPP {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraIotHoppingIvl:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:HOPP \n
		Sets the narrowband hopping interval. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: hopping_interval: H1| H2| H4| H5| H8| H10| H16| H20| H40"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:HOPP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraIotHoppingIvl)
