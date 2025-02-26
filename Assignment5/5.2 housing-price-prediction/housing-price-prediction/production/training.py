import logging
import os.path as op
import mlflow
import mlflow.sklearn
from ta_lib.core.api import (
    get_dataframe,
    get_feature_names_from_column_transformer,
    get_package_path,
    load_dataset,
    load_pipeline,
    register_processor,
    save_pipeline,
    DEFAULT_ARTIFACTS_PATH
)
from ta_lib.regression.api import SKLStatsmodelOLS
from ta_lib.hyperparm_tuning.tuner import optimize_hyperparameters

logger = logging.getLogger(__name__)

@register_processor("model-gen", "train-model")
def train_model(context, params):
    artifacts_folder = DEFAULT_ARTIFACTS_PATH

    input_features_ds = "train/sales/features"
    input_target_ds = "train/sales/target"

    # load training datasets
    train_X = load_dataset(context, input_features_ds)
    train_y = load_dataset(context, input_target_ds)

    # load pre-trained feature pipelines and other artifacts
    curated_columns = load_pipeline(op.join(artifacts_folder, "curated_columns.joblib"))
    features_transformer = load_pipeline(op.join(artifacts_folder, "features.joblib"))

    # sample data if needed. Useful for debugging/profiling purposes.
    sample_frac = params.get("sampling_fraction", None)
    if sample_frac is not None:
        logger.warn(f"The data has been sample by fraction: {sample_frac}")
        sample_X = train_X.sample(frac=sample_frac, random_state=context.random_seed)
    else:
        sample_X = train_X
    sample_y = train_y.loc[sample_X.index]

    # transform the training data
    train_X = get_dataframe(
        features_transformer.fit_transform(train_X, train_y),
        get_feature_names_from_column_transformer(features_transformer),
    )
    train_X = train_X[curated_columns]

    # Call the hyperparameter tuning function
    search_space = {
        "alpha": [0.01, 1.0],
        "l1_ratio": [0.0, 1.0],
    }
    best_params = optimize_hyperparameters(
        study_name="hyperparameter_study",
        storage=None,
        n_trials=10,
        search_space=search_space,
        context=context,
        params=params,
        X=train_X,
        y=train_y.values.ravel()
    )

    # Retrieve the best pipeline and hyperparameters
    best_pipeline = best_params["pipeline"]
    best_hyperparameters = best_params["best_params"]
    print('best_hyperparameters',best_hyperparameters)

    # fit the best pipeline
    best_pipeline.fit(train_X, train_y.values.ravel())

    # save fitted training pipeline
    save_pipeline(
        best_pipeline, op.abspath(op.join(artifacts_folder, "train_pipeline.joblib"))
    )

    with mlflow.start_run(run_name="train_model"):
        # Log the MLflow parameters
        mlflow.log_params(params)
        mlflow.log_params(best_hyperparameters)

        # Log the artifacts
        mlflow.log_artifact(op.join(artifacts_folder, "curated_columns.joblib"))
        mlflow.log_artifact(op.join(artifacts_folder, "features.joblib"))
        mlflow.log_artifact(op.abspath(op.join(artifacts_folder, "train_pipeline.joblib")))
        print('completed')
