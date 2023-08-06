from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tbasis:
	"""Tbasis commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbasis", core, parent)

	def set(self, time_basis: enums.TimeBasis, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GPS<ST>:TOAData:TBASis \n
		Determines the timebase used to enter the time of assistance data parameters. \n
			:param time_basis: UTC| GPS| GST| GLO| BDT| NAV
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.enum_scalar_to_str(time_basis, enums.TimeBasis)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS{stream_cmd_val}:TOAData:TBASis {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TimeBasis:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GPS<ST>:TOAData:TBASis \n
		Determines the timebase used to enter the time of assistance data parameters. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: time_basis: UTC| GPS| GST| GLO| BDT| NAV"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS{stream_cmd_val}:TOAData:TBASis?')
		return Conversions.str_to_scalar_enum(response, enums.TimeBasis)
