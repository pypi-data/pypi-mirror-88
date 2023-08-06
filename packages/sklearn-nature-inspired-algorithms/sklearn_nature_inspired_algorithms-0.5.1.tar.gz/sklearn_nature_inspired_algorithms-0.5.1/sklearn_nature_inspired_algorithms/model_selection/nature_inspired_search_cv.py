import numpy as np

from ._param_grid import ParamGrid
from ._parameter_search_benchmark import ParameterSearchBenchmark
from ._stagnation_stopping_task import StagnationStoppingTask

from NiaPy.algorithms.basic import FireflyAlgorithm, BatAlgorithm, GreyWolfOptimizer
from NiaPy.algorithms.modified import HybridBatAlgorithm, HybridSelfAdaptiveBatAlgorithm

from sklearn.model_selection._search import BaseSearchCV

SUPPORTED_ALGORITHMS = ['fa', 'gwo', 'ba', 'hba', 'hsaba']


class NatureInspiredSearchCV(BaseSearchCV):
    def _run_search(self, evaluate_candidates):
        self.__print_run_search_log()

        benchmark = ParameterSearchBenchmark(evaluate_candidates, self.__param_grid)

        self.optimization_logs_ = []

        for i in range(1, self.runs_ + 1):
            def iteration_finished_callback(iteration, stagnation_gen_count):
                stagnation = f' | Stagnation {stagnation_gen_count}'

                if self.__max_stagnating_gen > 1:
                    stagnation = f'{stagnation}/{self.__max_stagnating_gen}'

                if self.__nia_verbose > 1:
                    print(f'Run {i}/{self.runs_}, Iteration {iteration}/{self.__n_gen}{stagnation}'
                          f' | There were {benchmark.evaluation_count} candidates trained until now')

            task = StagnationStoppingTask(
                length=len(self.__param_grid),
                n_gen=self.__n_gen,
                max_stagnating_gen=self.__max_stagnating_gen,
                benchmark=benchmark,
                iteration_finished_callback=iteration_finished_callback
            )

            self.__algorithm.run(task=task)

            if self.__algorithm.exception:
                raise self.__algorithm.exception

            # invert scores in the optimization logs
            self.optimization_logs_.append([(log[0], log[1] * -1) for log in task.optimization_logs_])

            if self.__nia_verbose > 0:
                print(f'Run {i}/{self.runs_} finished')

        candidates = benchmark.evaluation_count

        if self.__cv is None:
            print(f'Optimization finished, {candidates} candidates were fitted')
        else:
            fits = candidates * self.__cv
            print(f'Optimization finished, {candidates} candidates were fitted (totalling {fits} fits)')

    def __init__(self, estimator, param_grid, algorithm='hba', population_size=50, max_n_gen=100, runs=3,
                 max_stagnating_gen=20, scoring=None, n_jobs=None, iid='deprecated', refit=True, cv=None, verbose=0,
                 random_state=None,
                 pre_dispatch='2*n_jobs', error_score=np.nan, return_train_score=True):
        super().__init__(estimator, scoring, n_jobs, iid, refit, cv, 0, pre_dispatch, error_score,
                         return_train_score)

        self.__n_gen = max_n_gen
        self.__max_stagnating_gen = max_stagnating_gen
        self.__param_grid = ParamGrid(param_grid)
        self.__algorithm = self.__get_algorithm(algorithm, population_size, random_state)
        self.__nia_verbose = verbose
        self.__cv = cv

        self.runs_ = runs
        self.optimization_logs_ = None

    def __print_run_search_log(self):
        candidates = self.__param_grid.get_number_of_candidates()

        if self.cv is not None:
            print(f'Fitting {self.cv} folds for some of the {candidates} candidates, '
                  f'which might total in {candidates * self.cv} fits')
        else:
            print(f'Fitting at most {candidates} candidates')

    @staticmethod
    def __get_algorithm(algorithm, population_size, random_state):
        if isinstance(algorithm, str):
            if algorithm not in SUPPORTED_ALGORITHMS:
                raise ValueError(f'"{algorithm}" is not in supported algorithms: {", ".join(SUPPORTED_ALGORITHMS)}')

            algorithm_obj = None

            if algorithm == 'fa':
                algorithm_obj = FireflyAlgorithm(seed=random_state)
                algorithm_obj.setParameters(alpha=1, betamin=1, gamma=2)
            elif algorithm == 'ba':
                algorithm_obj = BatAlgorithm(seed=random_state)
                algorithm_obj.setParameters(A=0.9, r=0.1, Qmin=0.0, Qmax=2.0)
            elif algorithm == 'hba':
                algorithm_obj = HybridBatAlgorithm(seed=random_state)
                algorithm_obj.setParameters(A=0.9, r=0.1, Qmin=0.0, Qmax=2.0)
            elif algorithm == 'hsaba':
                algorithm_obj = HybridSelfAdaptiveBatAlgorithm(seed=random_state)
                algorithm_obj.setParameters(A=0.9, r=0.1, Qmin=0.0, Qmax=2.0)
            elif algorithm == 'gwo':
                algorithm_obj = GreyWolfOptimizer(seed=random_state)

            algorithm_obj.setParameters(NP=population_size)

            return algorithm_obj

        return algorithm
