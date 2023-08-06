from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToWeek:
	"""ToWeek commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("toWeek", core, parent)

	def set(self, tow: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:TOAData:TOWeek \n
		Enabled for GPS timebase (method RsSmbv.Source.Bb.Gnss.AdGeneration.Gps.ToaData.Tbasis.set) . Determines the Time of Week
		(TOW) the assistance data is generated for. \n
			:param tow: integer Range: -604800 to 604800
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(tow)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:TOAData:TOWeek {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:TOAData:TOWeek \n
		Enabled for GPS timebase (method RsSmbv.Source.Bb.Gnss.AdGeneration.Gps.ToaData.Tbasis.set) . Determines the Time of Week
		(TOW) the assistance data is generated for. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: tow: integer Range: -604800 to 604800"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:TOAData:TOWeek?')
		return Conversions.str_to_int(response)
