from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Npar:
	"""Npar commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: AntennaPortIx, default value after init: AntennaPortIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("npar", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antennaPortIx_get', 'repcap_antennaPortIx_set', repcap.AntennaPortIx.Nr1)

	def clone(self) -> 'Npar':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Npar(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_antennaPortIx_set(self, enum_value: repcap.AntennaPortIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AntennaPortIx.Default
		Default value after init: AntennaPortIx.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antennaPortIx_get(self) -> repcap.AntennaPortIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, npar: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, antennaPortIx=repcap.AntennaPortIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:NPAR<AP> \n
		Sets the resource index for the supported PUCCH formats. \n
			:param npar: integer n(x) _PUCCH_max depends on the PUCCH format; to query the value, use the corresponding command, for example method RsSmbv.Source.Bb.Eutra.Ul.Pucch.N1Emax.get_. Range: 0 to n(x) _PUCCH_max
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param antennaPortIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Npar')"""
		param = Conversions.decimal_value_to_str(npar)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		antennaPortIx_cmd_val = self._base.get_repcap_cmd_value(antennaPortIx, repcap.AntennaPortIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:NPAR{antennaPortIx_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, antennaPortIx=repcap.AntennaPortIx.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:NPAR<AP> \n
		Sets the resource index for the supported PUCCH formats. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param antennaPortIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Npar')
			:return: npar: integer n(x) _PUCCH_max depends on the PUCCH format; to query the value, use the corresponding command, for example method RsSmbv.Source.Bb.Eutra.Ul.Pucch.N1Emax.get_. Range: 0 to n(x) _PUCCH_max"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		antennaPortIx_cmd_val = self._base.get_repcap_cmd_value(antennaPortIx, repcap.AntennaPortIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:NPAR{antennaPortIx_cmd_val}?')
		return Conversions.str_to_int(response)
