from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ndmrs:
	"""Ndmrs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: NdmrsLayer, default value after init: NdmrsLayer.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ndmrs", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_ndmrsLayer_get', 'repcap_ndmrsLayer_set', repcap.NdmrsLayer.Nr0)

	def clone(self) -> 'Ndmrs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ndmrs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_ndmrsLayer_set(self, enum_value: repcap.NdmrsLayer) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to NdmrsLayer.Default
		Default value after init: NdmrsLayer.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_ndmrsLayer_get(self) -> repcap.NdmrsLayer:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def get(self, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default, ndmrsLayer=repcap.NdmrsLayer.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:PUSCh:DRS:NDMRs<LAYER> \n
		Queries the parameter n(2) _DMRS,λ (Layer λ) . \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param ndmrsLayer: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ndmrs')
			:return: ndmrs: integer Range: 0 to 11"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		ndmrsLayer_cmd_val = self._base.get_repcap_cmd_value(ndmrsLayer, repcap.NdmrsLayer)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUSCh:DRS:NDMRs{ndmrsLayer_cmd_val}?')
		return Conversions.str_to_int(response)
