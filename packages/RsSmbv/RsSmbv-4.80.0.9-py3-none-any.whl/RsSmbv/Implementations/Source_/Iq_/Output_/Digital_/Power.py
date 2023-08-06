from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Power_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def get_level(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:LEVel \n
		Enters the RMS level of the output signal. \n
			:return: level: float Range: -80 to 0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:LEVel \n
		Enters the RMS level of the output signal. \n
			:param level: float Range: -80 to 0
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:LEVel {param}')

	def get_pep(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:PEP \n
		Enters the peak level of the output signal relative to full scale of 0.5 V (in terms of dB full scale) . \n
			:return: pep: float Range: -80 to 0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:PEP?')
		return Conversions.str_to_float(response)

	def set_pep(self, pep: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:PEP \n
		Enters the peak level of the output signal relative to full scale of 0.5 V (in terms of dB full scale) . \n
			:param pep: float Range: -80 to 0
		"""
		param = Conversions.decimal_value_to_str(pep)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:PEP {param}')

	def get_state(self) -> bool:
		"""[SOURce]:IQ:OUTPut:DIGital:POWer:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce:IQ:OUTPut:DIGital:POWer:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:POWer:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:POWer:STATe {param}')

	# noinspection PyTypeChecker
	def get_via(self) -> enums.IqOutDispViaType:
		"""[SOURce]:IQ:OUTPut:DIGital:POWer:VIA \n
		Selects the respective level entry field for the I/Q output. \n
			:return: via: PEP| LEVel
		"""
		response = self._core.io.query_str('SOURce:IQ:OUTPut:DIGital:POWer:VIA?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutDispViaType)

	def set_via(self, via: enums.IqOutDispViaType) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:POWer:VIA \n
		Selects the respective level entry field for the I/Q output. \n
			:param via: PEP| LEVel
		"""
		param = Conversions.enum_scalar_to_str(via, enums.IqOutDispViaType)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:POWer:VIA {param}')
