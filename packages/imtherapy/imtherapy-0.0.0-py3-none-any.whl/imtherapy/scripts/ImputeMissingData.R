#----------------------------------------------------------------
# Impute missing data with mice
# See: https://datasciencebeginners.com/2018/11/11/a-brief-introduction-to-mice-r-package/
#----------------------------------------------------------------

# library imports
library(mice)


# variable loads
merged_feature_file = {{ in.merged_features | r }}
outdir = {{ job.outdir | str | r }}
survs = {{ args.survs | r }}
outfile = {{ out.outfile | r }}
# This is ensured to be single outcome
outcome = {{ args.outcome | r }}
outcome_positive = {{ args.outcome_positive | r }}

# data loads
data = read.table(
    merged_feature_file,
    sep="\t",
    header=TRUE,
    row.names=1,
    check.names=FALSE
)
survdata = NULL
if (length(survs) > 0) {
    survdata = data[, survs]
}
data = data[, setdiff(colnames(data), survs)]

for (feat in colnames(data)) {
    # mice can't impute these types
    if (class(data[[feat]]) %in% c('logical', 'character')) {
        data[[feat]] = as.factor(data[[feat]])
    }
}

# logics
missing_fig = file.path(outdir, 'missing.png')
png(missing_fig, res=300, width=1000, height=1000)
md.pattern(data)
dev.off()

imputed = mice(data, m=5, seed=8525)
impute_method_file = file.path(outdir, 'impute-methods.txt')
impute_method = as.data.frame(imputed$method)
impute_method = data.frame(Variable=rownames(impute_method), Method=impute_method[,1])
write.table(
    impute_method,
    impute_method_file,
    col.names = TRUE,
    row.names = FALSE,
    sep="\t",
    quote=FALSE
)

outdata = complete(imputed)

write.table(cbind(outdata, survdata), outfile, row.names=TRUE, col.names=TRUE, sep="\t", quote=FALSE)
