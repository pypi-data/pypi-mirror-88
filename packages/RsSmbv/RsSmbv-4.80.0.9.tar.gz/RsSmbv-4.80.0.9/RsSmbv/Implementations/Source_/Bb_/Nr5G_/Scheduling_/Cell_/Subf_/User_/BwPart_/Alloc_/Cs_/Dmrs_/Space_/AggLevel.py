from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import enums
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AggLevel:
	"""AggLevel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aggLevel", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, spaceIx=repcap.SpaceIx.Default) -> enums.AllocDciaGgLvl:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DMRS:SPACe<S2US>:AGGLevel \n
		Queries the possible aggregation levels. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param spaceIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Space')
			:return: aggr_level: AL1| AL2| AL4| AL8| AL16"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		spaceIx_cmd_val = self._base.get_repcap_cmd_value(spaceIx, repcap.SpaceIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DMRS:SPACe{spaceIx_cmd_val}:AGGLevel?')
		return Conversions.str_to_scalar_enum(response, enums.AllocDciaGgLvl)
