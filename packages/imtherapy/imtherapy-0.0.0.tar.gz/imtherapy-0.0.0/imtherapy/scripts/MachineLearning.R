# library imports
library(mlr3)
library(mlr3learners)
library(mlr3filters)
library(future)

# variables load
selected_feature_file = {{in.selected_features | r }}
outdir = {{out.outdir | r}}
ncores = {{args.ncores | r}}
survs = {{args.survs | r}}
outcome = {{ args.outcome | r }}
outcome_positive = {{args.outcome_positive | r}}
rsmp_method = {{args.resample | r}}
model = {{args.model | r}}
model_name = {{args.model_name | r}}
factorize_chars = {{args.factorize_chars | r}}

plan('multisession', workers=ncores)
dir.create(outdir, showWarnings = FALSE)

if (rsmp_method[1] == 'cv') {
    resampling = rsmp("cv", folds = as.integer(rsmp_method[2]))
} else if (rsmp_method[1] == 'loo') {
    resampling = rsmp("loo")
} else if (rsmp_method[1] == 'repeated_cv') {
    resampling = rsmp("repeated_cv",
                      repeats = as.integer(rsmp_method[2]),
                      folds = as.integer(rsmp_method[3]))
} else {
    resampling = rsmp("holdout", ratio = as.numeric(rsmp_method[2]))
}

# data loads
outcome_data = read.table(
    selected_feature_file,
    sep="\t",
    header=TRUE,
    row.names=1,
    check.names=FALSE
)
featdata = outcome_data[, setdiff(colnames(outcome_data), c(outcome, survs))]
if (factorize_chars) {
    for (feat in colnames(featdata)) {
        if (class(featdata[[feat]]) == 'character') {
            featdata[[feat]] = as.factor(featdata[[feat]])
        }
        if (class(featdata[[feat]]) == 'factor') {
            featdata[[feat]] = as.numeric(featdata[[feat]])
        }
    }
}
outcome_data = outcome_data[, outcome, drop=FALSE]

# See if importance available for this model
lrner = mlr_learners$get(model)
imp_avail = 'importance' %in% names(lrner)

# logic
do_one_outcome = function(i, outc) {
    outcomedir = file.path(outdir, sprintf('outcome-%s', outc))
    preddir = file.path(outcomedir, 'predictions')
    dir.create(outcomedir, showWarnings = FALSE)
    dir.create(preddir, showWarnings = FALSE)

    taskdata = cbind(featdata, outcome_data[, outc, drop=FALSE])
    taskdata = taskdata[complete.cases(taskdata), ]
    task = TaskClassif$new(
        id=outc,
        backend=taskdata,
        target=outc,
        positive=as.character(outcome_positive[i])
    )
    if (imp_avail) {
        if (model == 'classif.ranger') {
            learner = lrn(model, predict_type="prob", importance = "impurity")
        } else {
            learner = lrn(model, predict_type="prob")
        }
        resampler = resample(task, learner, resampling, store_models=TRUE)
        filter = flt("importance", learner = learner)
        importance = filter$calculate(task)
    } else {
        learner = lrn(model, predict_type="prob")
        resampler = resample(task, learner, resampling, store_models=TRUE)
        importance = NULL
    }
    index = 1
    for (prediction in resampler$predictions()) {
        prediction = as.data.frame(as.data.table(prediction))
        prediction = prediction[, c(
            'row_id', 'truth', 'response', sprintf('prob.%s', outcome_positive[i])
        )]
        colnames(prediction)[ncol(prediction)] = 'prob'
        write.table(
            prediction,
            file.path(preddir, sprintf('prediction-%d.txt', index)),
            quote=FALSE,
            sep="\t",
            row.names=FALSE,
            col.names=TRUE
        )
        index = index + 1
    }
    # all_predictions = as.data.frame(as.data.table(resampler$prediction()))
    # all_predictions = all_predictions[, c(
    #     'row_id', 'truth', 'response', sprintf('prob.%s', outcome_positive[i])
    # )]
    # colnames(all_predictions)[ncol(all_predictions)] = 'prob'
    # write.table(
    #     as.data.table(resampler$prediction()),
    #     file.path(preddir, sprintf('all.txt', index)),
    #     quote=FALSE,
    #     sep="\t",
    #     row.names=FALSE,
    #     col.names=TRUE
    # )
    if (imp_avail) {
        write.table(
            as.data.table(importance),
            file.path(outcomedir, 'varimp.txt'),
            quote=FALSE,
            sep="\t",
            row.names=FALSE,
            col.names=TRUE
        )
    }

    rsmp_params = resampling$param_set$values
    metadata = data.frame(
        Model = model_name,
        Resampler = rsmp_method[1],
        Resampler_Params = paste(names(rsmp_params), rsmp_params, sep=': ', collapse = ', ')
    )
    metadata = as.data.frame(t(metadata))
    metadata = cbind(Name=rownames(metadata), Value=metadata[,1])

    write.table(
        metadata,
        file.path(outcomedir, 'meta.txt'),
        quote=FALSE,
        row.names=FALSE,
        sep="\t",
        col.names=TRUE
    )
}

for (i in seq_along(outcome)) {
    outcome_data[, outcome[i]] = as.factor(outcome_data[, outcome[i]])
    do_one_outcome(i, outcome[i])
}
