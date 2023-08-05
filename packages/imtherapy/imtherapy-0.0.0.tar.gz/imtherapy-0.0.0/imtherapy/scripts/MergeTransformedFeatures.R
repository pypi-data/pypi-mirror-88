# library imports

# variable loads
transformed_feature_file = {{ in.transformed_features | r }}
outfile = {{ out.outfile | r }}

# load data
data = NULL
for (featfile in transformed_feature_file) {
    featdata = read.table(featfile, check.names=FALSE, row.names=1, header=TRUE)
    if (is.null(data)) {
        data = featdata
    } else {
        featcols = colnames(featdata)
        intersected_cols = intersect(colnames(data), featcols)
        if (length(intersected_cols) > 0) {
            warning(paste(
                'Overlapping features ignored:',
                paste(intersected_cols, collapse=', ')
            ))
        }
        data = cbind(data, featdata[, setdiff(featcols, intersected_cols)])
    }
}

write.table(data, outfile, col.names=TRUE, row.names=TRUE, sep="\t", quote=FALSE)
