infiles = {{in.infiles | r }}
outfile = {{out.outfile | r }}

outdata = NULL

for (infile in infiles) {
    indata = read.table(
        infile,
        header=TRUE,
        row.names=1,
        sep="\t",
        check.names=FALSE
    )
    if (is.null(outdata)) {
        outdata = indata
    } else {
        outdata = cbind(outdata, indata[rownames(outdata),, drop=FALSE])
    }
}

write.table(outdata, outfile, col.names=TRUE, row.names=TRUE, sep="\t", quote=FALSE)
