from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bsize:
	"""Bsize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bsize", core, parent)

	def set(self, dl_bwp_static_bsize: enums.PrbBundleSizeSet1, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:PREC:BSIZe \n
		Configures the static PRB bundle type. Only available if 'Precoding' is enabled and 'Static' is selected as 'PRB Bundling
		Type'. \n
			:param dl_bwp_static_bsize: N4| WIDeband| N2WB| N4WB N4 Default value. Static PRB bundle is set to N4. WIDeband Static PRB bundle is set to wideband. N2WB Static PRB bundle is set to N2 wideband. N4WB Static PRB bundle is set to N4 wideband.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(dl_bwp_static_bsize, enums.PrbBundleSizeSet1)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:PREC:BSIZe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.PrbBundleSizeSet1:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:PREC:BSIZe \n
		Configures the static PRB bundle type. Only available if 'Precoding' is enabled and 'Static' is selected as 'PRB Bundling
		Type'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: dl_bwp_static_bsize: N4| WIDeband| N2WB| N4WB N4 Default value. Static PRB bundle is set to N4. WIDeband Static PRB bundle is set to wideband. N2WB Static PRB bundle is set to N2 wideband. N4WB Static PRB bundle is set to N4 wideband."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:PREC:BSIZe?')
		return Conversions.str_to_scalar_enum(response, enums.PrbBundleSizeSet1)
