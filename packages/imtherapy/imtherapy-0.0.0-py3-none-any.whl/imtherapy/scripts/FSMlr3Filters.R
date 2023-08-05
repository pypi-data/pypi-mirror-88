library(mlr3)
library(mlr3filters)
library(mlr3learners)
library(future)
library(dplyr)
library(scales)
library(ggplot2)

infile = {{in.infile | r }}
outfile = {{out.outfile | r }}
outdir = {{job.outdir | r }}
filter_method = {{args.filter | r }}
learner = {{ args.learner | r }}
params = {{ args.params | r }}
cutoff = {{args.cutoff | r }}
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
data[, outcome] = as.factor(data[, outcome])

task = TaskClassif$new(
    id=outcome,
    backend=data,
    target=outcome,
    positive=as.character(outcome_positive)
)
importance_filter = function() {
    lrn = lrn(learner, importance = "impurity")
    filter = flt("importance", learner = lrn)

    filter
}

non_importance_filter = function() {
    filter = flt(filter_method)
    filter$params_set$values = params

    filter
}

if (filter_method == 'importance') {
    filtered = importance_filter()
} else {
    filtered = non_importance_filter()
}

filtered$calculate(task)
fs_data = as.data.table(filtered) %>%
    mutate(score = rescale(score), selected = score >= cutoff)

fs_file = file.path(outdir, 'feature-selection.txt')
write.table(
    fs_data,
    fs_file,
    row.names = FALSE,
    col.names = TRUE,
    quote = FALSE,
    sep = "\t"
)

# plot
fs_plot = file.path(outdir, 'feature-selection.png')
g = ggplot(fs_data, aes(x=reorder(feature, score), y=score, fill=selected)) +
    geom_bar(stat="identity") +
    coord_flip() +
    theme_classic()

png(fs_plot, res=300, width=1000, height=1000)
print(g)
dev.off()

selected_features = fs_data %>% filter(selected) %>% select(feature)
selected_features = selected_features$feature

outdata = rawdata[, c(selected_features, survs, outcome)]
write.table(
    outdata,
    outfile,
    row.names = TRUE,
    col.names = TRUE,
    quote = FALSE,
    sep = "\t"
)

