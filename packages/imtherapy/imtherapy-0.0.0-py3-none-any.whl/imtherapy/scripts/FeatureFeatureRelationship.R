# library imports
library(ggplot2)
library(GGally)
library(tidystats)

# variable loads
selected_feature_file = {{ in.selected_features | r }}
merged_feature_file = {{ in.merged_features | r}}
outdir = {{ out.outdir | r }}
features = {{ args['features'] | r }}
survs = {{ args.survs | r }}
outcome = {{ args.outcome | r }}
non_feat_cols = c(survs, outcome)

global_plot = file.path(outdir, "global.png")

dir.create(outdir, showWarnings = FALSE)

# loading data
selected_feature_data = read.table(selected_feature_file, check.names=FALSE)
merged_feature_data = read.table(merged_feature_file, check.names=FALSE)
if (length(features) == 0) {
    features = setdiff(colnames(selected_feature_data), non_feat_cols)
}
data = cbind(
    selected_feature_data,
    merged_feature_data[, setdiff(colnames(merged_feature_data), colnames(selected_feature_data))]
)
data = data[, features]

# all pairs
n_features = length(features)
if (n_features < 2) {
    stop("There are less than 2 features selected.")
}
pairs = combn(features, 2, list)

# global view
png(global_plot, res=300, width=400*n_features, height=400*n_features)
ggpairs(data)
dev.off()

data_type = function(feat) {
    if (class(data[[feat]]) == 'factor') {
        return('factor')
    } else if (class(data[[feat]]) == 'logical') {
        data[[feat]] = as.factor(data[[feat]])
        return('factor')
    } else {
        # number coded factors
        uniq_vals = unique(data[[feat]])
        if (length(uniq_vals) <= 5) {
            data[[feat]] = as.factor(data[[feat]])
            return('factor')
        }
        return('numeric')
    }
}

save_model = function(model, outfile) {
    df = as.data.frame(t(as.data.frame(tidy_stats(model))))
    df = data.frame(Name=rownames(df), Value=df[, 1])
    write.table(
        df,
        outfile,
        col.names = T,
        row.names = F,
        sep = "\t",
        quote = F
    )
}

cat_cat_pair = function(feat1, feat2, pair_dir) {
    cont_table = table(data[, c(feat1, feat2)])
    df = as.data.frame.matrix(cont_table)
    df = cbind(data.frame(name7584745=rownames(df)), df)
    colnames(df)[1] = paste0(feat1, '\\\\', feat2)

    write.table(
        df,
        file.path(pair_dir, 'Contingency_Table.txt'),
        col.names = T,
        row.names = F,
        sep = "\t",
        quote = F
    )

    fisher_result = fisher.test(cont_table)
    save_model(fisher_result, file.path(pair_dir, 'Fisher`s_Exact_Test.txt'))

    chi_result = chisq.test(cont_table)
    save_model(chi_result, file.path(pair_dir, 'Chi2_Test.txt'))
}

cat_cont_pair = function(feat1, feat2, pair_dir) {
    # plot
    g = ggplot(data[, c(feat1, feat2)], aes_string(x=feat1, y=feat2)) +
        geom_boxplot() +
        geom_jitter(shape=16, position=position_jitter(0.2)) +
        xlab(feat1) +
        ylab(feat2) +
        theme_classic()
    png(file.path(pair_dir, 'Boxplot.png'), res=300, width=1000, height=1000)
    print(g)
    dev.off()

    # statistical tests
    # parametric
    # test mean
    aov_test = aov(as.formula(paste(feat2, '~', feat1)), data)
    save_model(aov_test, file.path(pair_dir, 'ANOVA.txt'))
    if (length(levels(data[[feat1]])) == 2) {
        t_test = t.test(as.formula(paste(feat2, '~', feat1)), data)
        save_model(t_test, file.path(pair_dir, 'T_Test.txt'))
    }

    # non-parametric
    kruskal_test = kruskal.test(as.formula(paste(feat2, '~', feat1)), data)
    save_model(kruskal_test, file.path(pair_dir, 'Kruskal_Wallis.txt'))
    if (length(levels(data[[feat1]])) == 2) {
        wilcox_test = wilcox.test(as.formula(paste(feat2, '~', feat1)), data)
        save_model(wilcox_test, file.path(pair_dir, 'Mann-Whitney_U_Test.txt'))
    }

}

cont_cat_pair = function(feat1, feat2, pair_dir) {
    cat_cont_pair(feat2, feat1, pair_dir)
}

cont_cont_pair = function(feat1, feat2, pair_dir) {
    # plot
    g = ggplot(data[, c(feat1, feat2)], aes_string(x=feat1, y=feat2)) +
        geom_point() +
        geom_smooth(method = "lm", se = FALSE) +
        xlab(feat1) +
        ylab(feat2) +
        theme_classic()
    png(file.path(pair_dir, 'Scatter_Plot.png'), res=300, width=1000, height=1000)
    print(g)
    dev.off()

    # coefficient
    pcc = cor.test(data[[feat1]], data[[feat2]])
    save_model(pcc, file.path(pair_dir, 'Pearson`s_r.txt'))

    scc = cor.test(data[[feat1]], data[[feat2]], method='spearman')
    save_model(scc, file.path(pair_dir, 'Spearman`s_rho.txt'))

    kt = cor.test(data[[feat1]], data[[feat2]], method='kendall')
    save_model(scc, file.path(pair_dir, 'Kendall`s_tau.txt'))
}

# do for one pair
do_one_pair = function(feat1, feat2) {
    pair_dir = file.path(outdir, paste0(feat1, '--', feat2))
    dir.create(pair_dir, showWarnings=FALSE)

    data_type1 = data_type(feat1)
    data_type2 = data_type(feat2)

    if (data_type1 == 'factor') {
        if (data_type2 == 'factor') {
            cat_cat_pair(feat1, feat2, pair_dir)
        } else {
            cat_cont_pair(feat1, feat2, pair_dir)
        }
    } else {
        if (data_type2 == 'factor') {
            cont_cat_pair(feat1, feat2, pair_dir)
        } else {
            cont_cont_pair(feat1, feat2, pair_dir)
        }
    }
}

for (pair in pairs) {
    do_one_pair(pair[1], pair[2])
}
