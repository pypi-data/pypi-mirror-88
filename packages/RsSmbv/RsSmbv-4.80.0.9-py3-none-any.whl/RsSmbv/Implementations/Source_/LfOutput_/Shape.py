from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shape:
	"""Shape commands group definition. 10 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shape", core, parent)

	def clone(self) -> 'Shape':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Shape(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pulse(self):
		"""pulse commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulse'):
			from .Shape_.Pulse import Pulse
			self._pulse = Pulse(self._core, self._base)
		return self._pulse

	@property
	def trapeze(self):
		"""trapeze commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_trapeze'):
			from .Shape_.Trapeze import Trapeze
			self._trapeze = Trapeze(self._core, self._base)
		return self._trapeze

	@property
	def triangle(self):
		"""triangle commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_triangle'):
			from .Shape_.Triangle import Triangle
			self._triangle = Triangle(self._core, self._base)
		return self._triangle

	def set(self, shape: enums.LfShapeBfAmily, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:LFOutput<CH>:SHAPe \n
		Selects the waveform shape of the LF signal. \n
			:param shape: SINE| SQUare| PULSe| TRIangle| TRAPeze
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.enum_scalar_to_str(shape, enums.LfShapeBfAmily)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.LfShapeBfAmily:
		"""[SOURce<HW>]:LFOutput<CH>:SHAPe \n
		Selects the waveform shape of the LF signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: shape: SINE| SQUare| PULSe| TRIangle| TRAPeze"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.LfShapeBfAmily)
