import optuna
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def create_pipeline(hyperparameters):
    scaler = StandardScaler()
    model = ElasticNet(alpha=hyperparameters["alpha"], l1_ratio=hyperparameters["l1_ratio"])
    pipeline = Pipeline([("scaler", scaler), ("model", model)])
    return pipeline

def objective(trial, search_space, context, params, X, y):
    hyperparameters = {}
    for key in search_space:
        hyperparameters[key] = trial.suggest_uniform(key, search_space[key][0], search_space[key][1])
    pipeline = create_pipeline(hyperparameters)
    score = cross_val_score(pipeline, X, y, scoring="neg_root_mean_squared_error", cv=params["cv"])

    # Fit the pipeline on the training data
    pipeline.fit(X, y)

    # Save the pipeline in the trial's user attributes
    trial.set_user_attr("pipeline", pipeline)

    return score.mean()

def optimize_hyperparameters(study_name, storage, n_trials, search_space, context, params, X, y):
    study_name = study_name
    storage = storage
    sampler = optuna.samplers.TPESampler(seed=context.random_seed)
    study = optuna.create_study(
        study_name=study_name,
        storage=storage,
        sampler=sampler,
        direction="maximize",
        load_if_exists=True,
    )

    study.optimize(
        lambda trial: objective(trial, search_space, context, params, X, y),
        n_trials=n_trials,
        n_jobs=params["n_jobs"],
    )

    return {
    "pipeline": study.best_trial.user_attrs["pipeline"],
    "best_params": study.best_params,
    "best_value": study.best_value,
    }
