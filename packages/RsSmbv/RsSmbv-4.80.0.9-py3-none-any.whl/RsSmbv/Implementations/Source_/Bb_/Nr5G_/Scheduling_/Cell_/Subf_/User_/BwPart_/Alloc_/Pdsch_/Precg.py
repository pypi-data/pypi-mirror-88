from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Precg:
	"""Precg commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("precg", core, parent)

	def set(self, user_alloc_pdschp: enums.DlpRbBundlingGranularity, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:PRECG \n
		For PDSCH allocations, the precoding granularity can be adjusted. Precondition is that the precoding for the PDSCH is
		enabled under 'User/BWP Settings > DL BWP Config > PDSCH > General Settings > Static Bundle Size'. \n
			:param user_alloc_pdschp: N2| N4| WIDeband N2 Precoding granularity is set to N2. N4 Precoding granularity is set to N4. This setting is not available if: - method RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Pdsch.VpInter.set equals 2 or - method RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Pdsch.RbgSize.set equals Config1 and BWP size ≤ 36 RBs WIDeband Precoding granularity is set to wideband.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(user_alloc_pdschp, enums.DlpRbBundlingGranularity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:PRECG {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.DlpRbBundlingGranularity:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:PRECG \n
		For PDSCH allocations, the precoding granularity can be adjusted. Precondition is that the precoding for the PDSCH is
		enabled under 'User/BWP Settings > DL BWP Config > PDSCH > General Settings > Static Bundle Size'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: user_alloc_pdschp: N2| N4| WIDeband N2 Precoding granularity is set to N2. N4 Precoding granularity is set to N4. This setting is not available if: - method RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Pdsch.VpInter.set equals 2 or - method RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Pdsch.RbgSize.set equals Config1 and BWP size ≤ 36 RBs WIDeband Precoding granularity is set to wideband."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:PRECG?')
		return Conversions.str_to_scalar_enum(response, enums.DlpRbBundlingGranularity)
