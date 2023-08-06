from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dformat:
	"""Dformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dformat", core, parent)

	def set(self, data_format: enums.AcqDataFormatGlonass, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:ACQuisition:DFORmat \n
		No command help available \n
			:param data_format: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.enum_scalar_to_str(data_format, enums.AcqDataFormatGlonass)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:ACQuisition:DFORmat {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.AcqDataFormatGlonass:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:ACQuisition:DFORmat \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: data_format: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:ACQuisition:DFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.AcqDataFormatGlonass)
