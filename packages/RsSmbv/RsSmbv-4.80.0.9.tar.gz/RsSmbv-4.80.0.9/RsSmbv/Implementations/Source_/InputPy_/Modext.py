from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modext:
	"""Modext commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modext", core, parent)

	def clone(self) -> 'Modext':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modext(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_impedance'):
			from .Modext_.Impedance import Impedance
			self._impedance = Impedance(self._core, self._base)
		return self._impedance

	# noinspection PyTypeChecker
	def get_coupling(self) -> enums.AcDc:
		"""[SOURce<HW>]:INPut:MODext:COUPling \n
		Selects the coupling mode for an externally applied modulation signal. \n
			:return: coupling: AC| DC AC Passes the AC signal component of the modulation signal. DC Passes the modulation signal with both components, AC and DC.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:INPut:MODext:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.AcDc)

	def set_coupling(self, coupling: enums.AcDc) -> None:
		"""[SOURce<HW>]:INPut:MODext:COUPling \n
		Selects the coupling mode for an externally applied modulation signal. \n
			:param coupling: AC| DC AC Passes the AC signal component of the modulation signal. DC Passes the modulation signal with both components, AC and DC.
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.AcDc)
		self._core.io.write(f'SOURce<HwInstance>:INPut:MODext:COUPling {param}')
