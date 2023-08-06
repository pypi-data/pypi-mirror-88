from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, frc_type: enums.FrcType, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:FRC:TYPE \n
		Selects the fixed reference measurement channel (FRC) . The currently available FRCs depend on the selected BWP
		subcarrier spacing SCS) and selected number of resource blocks. \n
			:param frc_type: FR1A11| FR1A12| FR1A13| FR1A14| FR1A15| FR1A16| FR1A17| FR1A18| FR1A19| FR2A11| FR2A12| FR2A13| FR2A14| FR2A15| FR1A21| FR1A22| FR1A23| FR1A24| FR1A25| FR1A26| NA| FR1A38| FR1A39| FR1A310| FR1A311| FR1A312| FR1A313| FR1A314| FR1A322| FR1A323| FR1A324| FR1A325| FR1A326| FR1A327| FR1A328| FR1A48| FR1A49| FR1A410| FR1A411| FR1A412| FR1A413| FR1A414| FR1A422| FR1A423| FR1A424| FR1A425| FR1A426| FR1A427| FR1A428| FR1A58| FR1A59| FR1A510| FR1A511| FR1A512| FR1A513| FR1A514| FR1A331| FR1A332| FR2A31| FR2A32| FR2A33| FR2A34| FR2A35| FR2A36| FR2A37| FR2A38| FR2A39| FR2A310| FR2A311| FR2A312| FR2A41| FR2A42| FR2A43| FR2A44| FR2A45| FR2A46| FR2A47| FR2A48| FR2A49| FR2A410| FR2A51| FR2A52| FR2A53| FR2A54| FR2A55| FR2A313| FR2A314| FR2A315| FR2A316| FR2A317| FR2A318| FR2A319| FR2A320| FR2A321| FR2A322| FR2A323| FR2A324| FR2A411| FR2A412| FR2A413| FR2A414| FR2A415| FR2A416| FR2A417| FR2A418| FR2A419| FR2A420| FR2A56| FR2A57| FR2A58| FR2A59| FR2A510
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(frc_type, enums.FrcType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:FRC:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.FrcType:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:FRC:TYPE \n
		Selects the fixed reference measurement channel (FRC) . The currently available FRCs depend on the selected BWP
		subcarrier spacing SCS) and selected number of resource blocks. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: frc_type: FR1A11| FR1A12| FR1A13| FR1A14| FR1A15| FR1A16| FR1A17| FR1A18| FR1A19| FR2A11| FR2A12| FR2A13| FR2A14| FR2A15| FR1A21| FR1A22| FR1A23| FR1A24| FR1A25| FR1A26| NA| FR1A38| FR1A39| FR1A310| FR1A311| FR1A312| FR1A313| FR1A314| FR1A322| FR1A323| FR1A324| FR1A325| FR1A326| FR1A327| FR1A328| FR1A48| FR1A49| FR1A410| FR1A411| FR1A412| FR1A413| FR1A414| FR1A422| FR1A423| FR1A424| FR1A425| FR1A426| FR1A427| FR1A428| FR1A58| FR1A59| FR1A510| FR1A511| FR1A512| FR1A513| FR1A514| FR1A331| FR1A332| FR2A31| FR2A32| FR2A33| FR2A34| FR2A35| FR2A36| FR2A37| FR2A38| FR2A39| FR2A310| FR2A311| FR2A312| FR2A41| FR2A42| FR2A43| FR2A44| FR2A45| FR2A46| FR2A47| FR2A48| FR2A49| FR2A410| FR2A51| FR2A52| FR2A53| FR2A54| FR2A55| FR2A313| FR2A314| FR2A315| FR2A316| FR2A317| FR2A318| FR2A319| FR2A320| FR2A321| FR2A322| FR2A323| FR2A324| FR2A411| FR2A412| FR2A413| FR2A414| FR2A415| FR2A416| FR2A417| FR2A418| FR2A419| FR2A420| FR2A56| FR2A57| FR2A58| FR2A59| FR2A510"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:FRC:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.FrcType)
