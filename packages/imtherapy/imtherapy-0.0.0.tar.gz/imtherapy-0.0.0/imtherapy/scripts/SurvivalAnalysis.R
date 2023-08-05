# library imports
library(survival) # 2.44-1.1
library(survminer) # 0.4.4.999
library(tidystats)

# variable loads
selected_feature_file = {{ in.selected_features | r }}
merged_feature_file = {{ in.merged_features | r}}
unidir = {{ out.unidir | r }}
multidir = {{ out.multidir | r }}
features = {{ args['features'] | r }}
survs = {{ args.survs | r }}
surv_unit = {{args['surv-unit'] | r}}
outcome = {{ args.outcome | r }}
non_feat_cols = c(survs, outcome)

dir.create(unidir, showWarnings = FALSE)
dir.create(multidir, showWarnings = FALSE)

# loading data
selected_feature_data = read.table(selected_feature_file, check.names=FALSE)
merged_feature_data = read.table(merged_feature_file, check.names=FALSE)
if (length(features) == 0) {
    features = setdiff(colnames(selected_feature_data), non_feat_cols)
    features = c(features, '__all__')
}
# allow combination of features to have multivariate cox-regression
feats = list()
feats_i = 1
all_feats = c()
for (feature in features) {
    if (grepl(",", feature, fixed = TRUE)) {
        feats[feats_i] = unlist(strsplit(feature, ","))
        all_feats = c(all_feats, feats[feats_i])
    } else {
        feats[feats_i] = feature
        all_feats = c(all_feats, feature)
    }
    feats_i = feats_i + 1
}
all_feats = unique(all_feats)
# surv_time1, surv_event1, surv_time2, surv_event2 to
# (surv_time1, surv_event1), (surv_time2, surv_event2)
surv_pairs = split(survs, ceiling(seq_along(survs)/2))

data = cbind(
    selected_feature_data,
    merged_feature_data[, setdiff(colnames(merged_feature_data), colnames(selected_feature_data))]
)
data = data[, setdiff(c(all_feats, survs), c(outcome, '__all__'))]
# Used to replace __all__
all_feats = setdiff(colnames(selected_feature_data), non_feat_cols)

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
    df = as.data.frame(t(model))
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

do_one_feature_and_surv = function(feature, surv) {
    if (length(feature) == 1 && feature == '__all__') {
        do_multi(all_feats, surv, dir_name = feature)
    } else if (length(feature) > 1) {
        do_multi(feature, surv, dir_name = paste(feature, collapse=","))
    } else {
        do_uni(feature, surv, dir_name = feature)
    }
}

surv_cut = function(feature, surv, by = "maxstat",
                    labels = c("low", "high")) {
    # by = mean, median, q25, q75, maxstat
    if (by == 'maxstat') {
        data_cut = surv_cutpoint(data, time = surv[1], event = surv[2],
                                 variables = feature)
        data_cat = surv_categorize(data_cut, variables = feature, labels = labels)
        return (data_cat[, feature])
    }

    vdata = as.vector(unlist(data[, feature]))
    vcut = by
    if (by == "mean") {
        vcut = mean(vdata, na.rm=TRUE)
    } else if (by == "median") {
        vcut = median(vdata, na.rm=TRUE)
    } else if (by == "q25") {
        vcut = quantile(vdata, .25, na.rm=TRUE)
    } else if (by == "q75") {
        vcut = quantile(vdata, .75, na.rm=TRUE)
    }
    icut = tryCatch({
        as.integer(median(which(vdata %in% vcut)))
    }, error = function(err) {
        0
    })
    return (sapply(seq_along(vdata), function(i) {
        if (is.na(vdata[i])) {
            NA
        } else if (vdata[i] < vcut) {
            labels[1]
        } else if (vdata[i] > vcut) {
            labels[2]
        } else if (i < icut) {
            labels[1]
        } else {
            labels[2]
        }
    }))
}

do_uni_cat = function(feature, surv, dir_path, cat_data = data) {
    fmula = as.formula(sprintf("Surv(%s, %s) ~ %s", surv[1], surv[2], feature))
    modfit = surv_fit(fmula, data = cat_data)
    model = data.frame(
        Var = feature,
        Method = "Kaplan Merier",
        Test = "LogRank",
        Groups = paste(
            unique(cat_data[, feature]), collapse = ', '
        ),
        DF = 1,
        Pvalue = surv_pvalue(modfit, data = cat_data)$pval
    )
    save_model(
        model,
        file.path(
            dir_path, sprintf('Kaplan_Meier@%s-%s.txt', surv[1], surv[2])
        )
    )

    png(
        file.path(dir_path, sprintf('Kaplan_Meier@%s-%s.png', surv[1], surv[2])),
        res=150, height=1000, width=1000
    )
    print(ggsurvplot(modfit, data = cat_data, risk.table = TRUE))
    dev.off()
}

do_uni_cont = function(feature, surv, dir_path) {
    cat_data = data[, surv]
    for (cutmethod in c('maxstat', 'mean', 'median', 'q25', 'q75')) {
        dpath = file.path(dir_path, cutmethod)
        dir.create(dpath, showWarnings = FALSE)

        cut_data = surv_cut(feature, surv, cutmethod)
        cat_data = data[, c(feature, surv)]
        cat_data[, feature] = cut_data
        do_uni_cat(feature, surv, dpath, cat_data = cat_data)
    }
}

do_multi = function(features, surv, dir_name) {
    dir_path = file.path(multidir, dir_name)
    dir.create(dir_path, showWarnings = FALSE)

    fmula = as.formula(
        sprintf('Surv(%s, %s) ~ %s', surv[1], surv[2], paste(features, collapse = '+'))
    )
    modfit = coxph(fmula, data = data)
    sumfit = summary(modfit)

    model <- data.frame(
        Var = paste(features, collapse = ', '),
        Method = "Cox Regression",
        Test = "Log Rank"
    )

    model <- cbind(
        model, sumfit$conf.int[, -2, drop = FALSE]
    )
    model$DF <- sumfit$logtest[2]
    model$Pvalue <- sumfit$logtest[3]

    colnames(model)[4:6] <- c("HR", "CI95_1", "CI95_2")

    save_model(model, file.path(dir_path, sprintf('Cox@%s-%s.txt', surv[1], surv[2])))
}

do_uni = function(feature, surv, dir_name) {
    dir_path = file.path(unidir, dir_name)
    dir.create(dir_path, showWarnings = FALSE)

    if (data_type(feature) == 'factor') {
        do_uni_cat(feature, surv, dir_path)
    } else {
        do_uni_cont(feature, surv, dir_path)
    }
}

for (feature in feats) {
    for (surv_pair in surv_pairs) {
        do_one_feature_and_surv(feature, surv_pair)
    }
}

