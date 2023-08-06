import numpy  # type: ignore
import scipy.integrate as integrate  # type: ignore
import scipy.optimize  # type: ignore
import scipy.special  # type: ignore
import logging
import warnings

from typing import Tuple


def energy(freq: float, delta: float) -> float:
	return numpy.sqrt(freq ** 2 + delta ** 2)


def gap_integrand_function(
	xi: float,
	temp: float,
	delta: float,
	mu_star: float
) -> float:
	big_e = energy(xi, delta)
	if temp == 0:
		return (1 / (2 * big_e)) * (2 * numpy.heaviside(big_e - mu_star, .5) - 1)
	return numpy.tanh((big_e - mu_star) / (2 * temp)) / (2 * big_e)


def gap_integral(
	temp: float,
	delta: float,
	mu_star: float,
	debye_frequency: float
) -> float:
	def integrand(xi: float) -> float:
		# the 2 here is to account for the symmetry in the integration range
		# to cut the integral to zero to omega_debyeh
		return 2 * gap_integrand_function(xi, temp, delta, mu_star)
	return integrate.quad(integrand, 0, debye_frequency)[0]


def equilibrium_gap(temp: float, debye_frequency: float, nv: float) -> float:
	return find_gap(temp, 0, debye_frequency, nv)


def find_gap(
	temp: float,
	mu_star: float,
	debye_frequency: float,
	nv: float
) -> float:
	nv_inv = 1 / nv
	sol = scipy.optimize.root(
		lambda d: gap_integral(temp, d, mu_star, debye_frequency) - nv_inv,
		x0=debye_frequency / (numpy.sinh(nv_inv))
	)
	return sol.x


# this is n * Delta_0, calling it n in this file for brevity
def n_integrand_function(
	xi: float, temp: float, delta: float, mu_star: float
) -> float:
	big_e = energy(xi, delta)
	left = scipy.special.expit((mu_star - big_e) / temp)
	right = scipy.special.expit(- big_e / temp)
	return left - right


# as above, this is brevity n * Delta_0
def n_integral(temp: float, delta: float, mu_star: float) -> float:
	def integrand(xi: float) -> float:
		return n_integrand_function(xi, temp, delta, mu_star)
	intermediate = 20 * numpy.sqrt(delta ** 2 + mu_star ** 2)
	lower = integrate.quad(integrand, 0, intermediate)[0]
	upper = integrate.quad(integrand, intermediate, numpy.inf)[0]
	return lower + upper


def find_gap_for_n(
	temp: float,
	n_bare: float,
	debye_frequency: float,
	nv: float
) -> Tuple[float, float]:
	n = n_bare * find_gap(0, 0, debye_frequency, nv)
	nv_inv = 1 / nv
	with warnings.catch_warnings():
		warnings.filterwarnings(
			"ignore",
			message="Creating an ndarray from ragged nested"
		)
		sol = scipy.optimize.root(
			lambda x: [
				gap_integral(temp, x[0], x[1], debye_frequency) - nv_inv,
				n_integral(temp, x[0], x[1]) - n
			],
			x0=[debye_frequency / (numpy.sinh(nv_inv)), 0]
		)
		logging.debug(sol)
		return sol.x
