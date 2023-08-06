from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApSelect:
	"""ApSelect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: AntennaSelect, default value after init: AntennaSelect.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apSelect", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antennaSelect_get', 'repcap_antennaSelect_set', repcap.AntennaSelect.Nr0)

	def clone(self) -> 'ApSelect':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApSelect(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_antennaSelect_set(self, enum_value: repcap.AntennaSelect) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AntennaSelect.Default
		Default value after init: AntennaSelect.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antennaSelect_get(self) -> repcap.AntennaSelect:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, pdsch_ap_sel: enums.Nr5GpdschAp, channel=repcap.Channel.Default, stream=repcap.Stream.Default, antennaSelect=repcap.AntennaSelect.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:[DMRS]:APSelect<S2US> \n
		Each layer of a PDSCH allocation is mapped to a certain antenna port. By the command the antenna ports are selected which
		are used for the transmission of the PDSCH allocation. \n
			:param pdsch_ap_sel: AP1000| AP1001| AP1002| AP1003| AP1004| AP1005| AP1006| AP1007| AP1008| AP1009| AP1010| AP1011
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param antennaSelect: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApSelect')"""
		param = Conversions.enum_scalar_to_str(pdsch_ap_sel, enums.Nr5GpdschAp)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		antennaSelect_cmd_val = self._base.get_repcap_cmd_value(antennaSelect, repcap.AntennaSelect)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:DMRS:APSelect{antennaSelect_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, antennaSelect=repcap.AntennaSelect.Default) -> enums.Nr5GpdschAp:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:[DMRS]:APSelect<S2US> \n
		Each layer of a PDSCH allocation is mapped to a certain antenna port. By the command the antenna ports are selected which
		are used for the transmission of the PDSCH allocation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param antennaSelect: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApSelect')
			:return: pdsch_ap_sel: AP1000| AP1001| AP1002| AP1003| AP1004| AP1005| AP1006| AP1007| AP1008| AP1009| AP1010| AP1011"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		antennaSelect_cmd_val = self._base.get_repcap_cmd_value(antennaSelect, repcap.AntennaSelect)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:DMRS:APSelect{antennaSelect_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GpdschAp)
