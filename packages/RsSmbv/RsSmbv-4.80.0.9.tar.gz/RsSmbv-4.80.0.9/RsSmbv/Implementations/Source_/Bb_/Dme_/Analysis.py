from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Analysis:
	"""Analysis commands group definition. 14 total commands, 1 Sub-groups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("analysis", core, parent)

	def clone(self) -> 'Analysis':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Analysis(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def gate(self):
		"""gate commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_gate'):
			from .Analysis_.Gate import Gate
			self._gate = Gate(self._core, self._base)
		return self._gate

	def get_efficiency(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:EFFiciency \n
		Queries the measured reply efficiency in percent. The measurement is the ratio of the number of measured valid reply
		pulse pairs to transmitted pulse pairs in a measurement cycle. \n
			:return: efficiency: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:EFFiciency?')
		return Conversions.str_to_float(response)

	def get_ia_factor(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:IAFactor \n
		Queries the internal adjustment factor, the mathematically calculated value of the time, when the pulse reaches its 50%
		level. \n
			:return: internal_adj_fact: float Range: 0 to 200
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:IAFactor?')
		return Conversions.str_to_float(response)

	def get_normalize(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:NORMalize \n
		Performs a normalization of the test setup. The delay due to the test setup is measured and subsequently considered in
		the reply measurements. \n
			:return: normalize: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:NORMalize?')
		return Conversions.str_to_bool(response)

	def get_ok(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:OK \n
		Queries if there are DME measurement values in the set measurement window. \n
			:return: status: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:OK?')
		return Conversions.str_to_bool(response)

	def get_power(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:POWer \n
		Queries the measured average peak level of all valid pulse pairs in a measurement cycle. \n
			:return: power: float Range: -200 to 200
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:POWer?')
		return Conversions.str_to_float(response)

	def get_pr_rate(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:PRRate \n
		Queries the measured mean pulse repetition rate of the DME ground station. All received pulses of the DME ground station
		are considered. \n
			:return: rate: float Range: 0 to 10000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:PRRate?')
		return Conversions.str_to_float(response)

	def get_psa_factor(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:PSAFactor \n
		Queries the power sensor adjustment factor determined during a normalization of the setup. You can normalize the setup
		with method RsSmbv.Source.Bb.Dme.Analysis.normalize. \n
			:return: pow_sens_adj_fact: float Range: 0 to 200
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:PSAFactor?')
		return Conversions.str_to_float(response)

	def get_rdistance(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:RDIStance \n
		Queries the measured average range distance of all valid pulse pairs in a measurement cycle. \n
			:return: range_distance: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:RDIStance?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:STATe \n
		Activates/deactivates the DME analysis. Activation requires that an R&S NRP-Z81 power sensor is connected to the R&S
		SMBV100B. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:STATe \n
		Activates/deactivates the DME analysis. Activation requires that an R&S NRP-Z81 power sensor is connected to the R&S
		SMBV100B. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ANALysis:STATe {param}')

	def get_time(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:TIME \n
		Queries the measured average reply delay of all valid pulse pairs in a measurement cycle. \n
			:return: time: float Range: -1E-3 to 1E-3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:TIME?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_ua_factor(self) -> enums.AvionicDmeUsedFact:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:UAFactor \n
		Sets which internal adjustment factor is used. \n
			:return: used_factor: INTernal| PSENsor INTernal The mathematically calculated value of the time, when the pulse reaches its 50% level. Query the internal adjustment factor with method RsSmbv.Source.Bb.Dme.Analysis.iaFactor PSENsor The adjustment factor measured during a normalization setup. Query the power sensor adjustment factor with method RsSmbv.Source.Bb.Dme.Analysis.psaFactor
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:UAFactor?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeUsedFact)

	def set_ua_factor(self, used_factor: enums.AvionicDmeUsedFact) -> None:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:UAFactor \n
		Sets which internal adjustment factor is used. \n
			:param used_factor: INTernal| PSENsor INTernal The mathematically calculated value of the time, when the pulse reaches its 50% level. Query the internal adjustment factor with method RsSmbv.Source.Bb.Dme.Analysis.iaFactor PSENsor The adjustment factor measured during a normalization setup. Query the power sensor adjustment factor with method RsSmbv.Source.Bb.Dme.Analysis.psaFactor
		"""
		param = Conversions.enum_scalar_to_str(used_factor, enums.AvionicDmeUsedFact)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ANALysis:UAFactor {param}')
