from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Btype:
	"""Btype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("btype", core, parent)

	def set(self, dl_bwp_prb_bundl_in: enums.PrbBundlingType, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:PREC:BTYPe \n
		Indicates the PRB bundle type and bundle sizes. If 'dynamic' is chosen, the actual bundle size set to use is indicated
		via DCI. Only available if 'Precoding' is enabled. The PRB bundling type supports the UE to reduce the computational
		effort to receive the information which PRBs use the same precoding. The UE only has to do channel estimation per PRB
		bundle not per PRB. Without this information, the UE has to decode all the information itself based on the DMRS. \n
			:param dl_bwp_prb_bundl_in: NOTC| STATic| DYNamic NOTC Default value, PRB bundling is not configured. STATic PRB bundling is set to static and can be adjusted by the 'Static Bundle Size'. DYNamic PRB bundling is set to dynamic and can be adjusted by the 'Bundle Size Set 1' and 'Bundle Size Set 2'.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(dl_bwp_prb_bundl_in, enums.PrbBundlingType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:PREC:BTYPe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.PrbBundlingType:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:PREC:BTYPe \n
		Indicates the PRB bundle type and bundle sizes. If 'dynamic' is chosen, the actual bundle size set to use is indicated
		via DCI. Only available if 'Precoding' is enabled. The PRB bundling type supports the UE to reduce the computational
		effort to receive the information which PRBs use the same precoding. The UE only has to do channel estimation per PRB
		bundle not per PRB. Without this information, the UE has to decode all the information itself based on the DMRS. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: dl_bwp_prb_bundl_in: NOTC| STATic| DYNamic NOTC Default value, PRB bundling is not configured. STATic PRB bundling is set to static and can be adjusted by the 'Static Bundle Size'. DYNamic PRB bundling is set to dynamic and can be adjusted by the 'Bundle Size Set 1' and 'Bundle Size Set 2'."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:PREC:BTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.PrbBundlingType)
