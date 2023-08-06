from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CycPrefix:
	"""CycPrefix commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cycPrefix", core, parent)

	def set(self, cyclic_prefix: enums.EuTraDuration, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:CYCPrefix \n
		If BB:EUTR:UL:CPC USER, sets the cyclic prefix for the selected subframe. \n
			:param cyclic_prefix: NORMal| EXTended
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(cyclic_prefix, enums.EuTraDuration)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:CYCPrefix {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EuTraDuration:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:CYCPrefix \n
		If BB:EUTR:UL:CPC USER, sets the cyclic prefix for the selected subframe. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: cyclic_prefix: NORMal| EXTended"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:CYCPrefix?')
		return Conversions.str_to_scalar_enum(response, enums.EuTraDuration)
