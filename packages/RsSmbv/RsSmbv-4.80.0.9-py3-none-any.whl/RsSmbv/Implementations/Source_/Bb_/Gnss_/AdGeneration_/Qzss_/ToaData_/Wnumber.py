from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wnumber:
	"""Wnumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wnumber", core, parent)

	def set(self, week_number: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:QZSS<ST>:TOAData:WNUMber \n
		Enabled for GPS timebase (method RsSmbv.Source.Bb.Gnss.AdGeneration.Qzss.ToaData.Tbasis.set) . Sets the week number (WN)
		the assistance data is generated for. \n
			:param week_number: integer Range: 0 to 9999.0*53
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.decimal_value_to_str(week_number)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:QZSS{stream_cmd_val}:TOAData:WNUMber {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:QZSS<ST>:TOAData:WNUMber \n
		Enabled for GPS timebase (method RsSmbv.Source.Bb.Gnss.AdGeneration.Qzss.ToaData.Tbasis.set) . Sets the week number (WN)
		the assistance data is generated for. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: week_number: integer Range: 0 to 9999.0*53"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:QZSS{stream_cmd_val}:TOAData:WNUMber?')
		return Conversions.str_to_int(response)
