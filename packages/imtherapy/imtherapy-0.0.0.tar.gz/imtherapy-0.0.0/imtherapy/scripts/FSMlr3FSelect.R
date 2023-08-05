library(mlr3)
library(mlr3fselect)
library(future)

infile = {{in.infile | r }}
outfile = {{out.outfile | r }}

resample = {{args.resample | r }}
learner = {{ args.learner | r }}
measure = {{ args.measure | r }}
terminator = {{args.terminator | r }}
selector = {{args.selector | r }}

if (resample[1] == 'cv') {
    resampling = rsmp("cv", folds = as.integer(resample[2]))
} else if (resample[1] == 'loo') {
    resampling = rsmp("loo")
} else if (resample[1] == 'repeated_cv') {
    resampling = rsmp("repeated_cv",
                      repeats = as.integer(resample[2]),
                      folds = as.integer(resample[3]))
} else {
    resampling = rsmp("holdout", ratio = as.numeric(resample[2]))
}

terminators = unlist(strsplit(terminator, ':', fixed=TRUE))
if (length(terminators) == 1) {
    terminator = trm(terminators[1])
} else if (terminators[1] == 'evals') {
    terminator = trm(terminators[1], n_evals = as.integer(terminators[2]))
} else { # support other terminators
    terminator = trm(terminators[1], as.integer(terminators[2]))
}

selectors = unlist(strsplit(selector, ':', fixed=TRUE))
if (length(selectors) == 1) {
    selector = fs(selectors[1])
} else if (selectors[1] == 'sequential') {
    selector = fs(selectors[1], max_features = as.integer(selectors[2]))
} else { # support other selectors
    selector = fs(selectors[1], as.integer(selectors[2]))
}

ncores = {{ args.ncores | r }}
outcome = {{ args.outcome | r }}
outcome_positive = {{ args.outcome_positive | r }}
survs = {{ args.survs | r }}

plan('multisession', workers=ncores)

rawdata = read.table(
    infile,
    sep="\t",
    header=TRUE,
    row.names=1,
    check.names=FALSE
)

data = rawdata[, setdiff(colnames(rawdata), survs)]
for (feat in colnames(data)) {
    # mice can't impute these types
    if (class(data[[feat]]) %in% c('logical', 'character')) {
        data[[feat]] = as.factor(data[[feat]])
    }
}

task = TaskClassif$new(
    id=outcome,
    backend=data,
    target=outcome,
    positive=as.character(outcome_positive)
)

learner = lrn(learner)
measure = msr(measure)
instance = FSelectInstanceSingleCrit$new(
    task = task,
    learner = learner,
    resampling = resampling,
    measure = measure,
    terminator = terminator
)
selector$optimize(instance)

selected_features = unlist(instance$result$features)

outdata = rawdata[, c(selected_features, survs, outcome)]
write.table(
    outdata,
    outfile,
    row.names = TRUE,
    col.names = TRUE,
    quote = FALSE,
    sep = "\t"
)

