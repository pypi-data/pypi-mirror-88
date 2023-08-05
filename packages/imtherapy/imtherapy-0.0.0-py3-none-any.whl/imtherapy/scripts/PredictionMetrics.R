# library imports
library(precrec)
library(ggplot2)
library(Metrics)
library(dplyr)

# variable loads
average = {{ args.average | r }}
outdir = {{ out.outdir | r }}
predirs = {{ in.predirs | r }}
outcomes = as.character({{ args.outcome | r }})
positive = as.character({{ args.outcome_positive | r }})
# A vector of directories with structure:
# results/
# |- outcome-*
#    |- meta.txt
#    |- varimp.txt (none if not available)
#    |- predictions/
#       |- prediction-1.txt (prediction of first iteration)
#       |- prediction-2.txt
#       |- ...

read_outcome_data = function(outcome_dir) {
    metafile = file.path(outcome_dir, "meta.txt")
    metadata = as.data.frame(t(read.table(metafile, header=TRUE, row.names=1, sep="\t")))

    varimp_file = file.path(outcome_dir, "varimp.txt")
    if (file.exists(varimp_file)) {
        vidata = read.table(varimp_file, header=TRUE, row.names=NULL, sep="\t")
    } else {
        vidata = NULL
    }

    pred_files = Sys.glob(file.path(outcome_dir, "predictions", "prediction-*.txt"))

    preddata = NULL
    for (pred_file in pred_files) {
        pred_fold = as.integer(gsub("prediction-", "", tools::file_path_sans_ext(basename(pred_file))))
        pred_tmp = read.table(pred_file, header=TRUE, row.names=NULL, sep="\t")
        pred_tmp = data.frame(
            score = pred_tmp$prob,
            label = pred_tmp$truth == positive,
            prediction = pred_tmp$response == positive,
            fold = pred_fold
        )
        if (is.null(preddata)) {
            preddata = pred_tmp
        } else {
            preddata = rbind(preddata, pred_tmp)
        }
    }

    return(list(metadata=metadata, vidata=vidata, preddata=preddata))

}

metrics_from_dataframe = function(df) {
    ret = data.frame(Name=character(), Full_Name=character(), Value=numeric())
    ret = rbind(ret, list(
        Name = 'ce',
        Full_Name = 'Classification Error',
        Value = ce(df$label, df$prediction)
    ))
    ret = rbind(ret, list(
        Name = 'accuracy',
        Full_Name = 'Accuracy',
        Value = accuracy(df$label, df$prediction)
    ))
    ret = rbind(ret, list(
        Name = 'f1',
        Full_Name = 'F1 Score',
        Value = f1(df$label, df$prediction)
    ))
    ret = rbind(ret, list(
        Name = 'auc',
        Full_Name = 'Area Under ROC Curve',
        Value = Metrics::auc(df$label, df$prediction)
    ))
    ret = rbind(ret, list(
        Name = 'logLoss',
        Full_Name = 'Mean Log Loss',
        Value = logLoss(df$label, df$prediction)
    ))
    ret = rbind(ret, list(
        Name = 'precision',
        Full_Name = 'Precision',
        Value = precision(df$label, df$prediction)
    ))
    ret = rbind(ret, list(
        Name = 'recall',
        Full_Name = 'Recall',
        Value = recall(df$label, df$prediction)
    ))

    ret
}

do_one_model_and_outcome = function(predir, outcome) {
    outcome_dir = file.path(predir, sprintf("outcome-%s", outcome))
    outcome_data = read_outcome_data(outcome_dir)

    metafile = file.path(outcome_dir, "meta.txt")
    dname = gsub(" ", "_", outcome_data$metadata$Model)

    odir = file.path(outdir, dname, sprintf("outcome-%s", outcome))
    dir.create(odir, showWarnings = FALSE, recursive=TRUE)
    file.copy(metafile, file.path(odir, 'meta.txt'))

    varimp_file = file.path(outcome_dir, "varimp.txt")
    if (file.exists(varimp_file)) {
        file.copy(varimp_file, file.path(odir, 'varimp.txt'))
        if (nrow(outcome_data$vidata) > 20) {
            vidata = outcome_data$vidata[1:20, , drop=FALSE]
        } else {
            vidata = outcome_data$vidata
        }

        g = ggplot(vidata,aes(x=reorder(feature, score), y=score)) +
            geom_bar(stat="identity", fill="#619CFF") +
            coord_flip() +
            theme_classic()

        png(file.path(odir, 'varimp.png'), res=300, width=1000, height=1000)
        print(g)
        dev.off()
    }

    # plot roc with format_nfold
    nfold_data = format_nfold(
        nfold_df = outcome_data$preddata,
        score_cols = "score",
        lab_col = "label",
        fold_col = "fold"
    )
    folds = unique(outcome_data$preddata$fold)
    cvcurves = evalmod(
        scores = nfold_data$scores,
        labels = nfold_data$labels,
        modnames = outcome_data$metadata$Model,
        dsids = folds,
        raw_curves = TRUE
    )
    png(file.path(odir, 'roc.png'), res=300, width=2000, height=1000)
    g = autoplot(cvcurves)
    print(g)
    dev.off()

    # see: https://mlr3.mlr-org.com/reference/Measure.html?q=average
    if (average == 'micro') {
        # use all from outcome_data$preddata as a single prediction object
        metrics = metrics_from_dataframe(outcome_data$preddata)
    } else { # 'macro'
        metrics = NULL
        for (fold in folds) {
            df = outcome_data$preddata[outcome_data$preddata$fold==fold, ]
            metric = metrics_from_dataframe(df)
            if (is.null(metrics)) {
                metrics = metric
            } else {
                metrics = rbind(metrics, metric)
            }

        }
        metrics = metrics %>% group_by(Name) %>% summarize(
            Score = mean(Value),
            Sd = sd(Value),
            CI95_1 = mean(Value) - qnorm(.975) * sd(Value) / sqrt(length(Value)),
            CI95_2 = mean(Value) + qnorm(.975) * sd(Value) / sqrt(length(Value))
        )
        #metrics = outcome_data$preddata %>% group_by(fold) %>% metrics_from_dataframe()
    }
    metrics_file = file.path(odir, 'metrics.txt')
    write.table(metrics, metrics_file, row.names=FALSE, col.names=TRUE, sep="\t", quote=FALSE)

    return(list(name=outcome_data$metadata$Model, data=outcome_data$preddata))
}

# logics
do_one_outcome = function(outcome) {
    # get all predictions to give a global plots and table

    scores = list()
    labels = list()
    modnames = c()
    for (predir in predirs) {
        meta = do_one_model_and_outcome(predir, outcome)
        scores = c(scores, list(meta$data$score))
        labels = c(labels, list(meta$data$label))
        modnames = c(modnames, meta$name)
    }

    if (length(predirs) > 1) {
        global_data = mmdata(do.call(join_scores, scores), do.call(join_labels, labels), modnames)
        global_roc = evalmod(global_data)

        png(file.path(outdir, sprintf('roc-%s.png', outcome)), res=300, width=2000, height=1000)
        g = autoplot(global_roc)
        print(g)
        dev.off()
    }
}

for (outcome in outcomes) {
    do_one_outcome(outcome)
}

