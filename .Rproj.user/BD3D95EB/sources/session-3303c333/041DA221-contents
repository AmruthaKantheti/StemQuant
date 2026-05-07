# 09_PanCancer_Model_Data_Export.R

# Load saved objects
gbm_expr <- readRDS("GBM_Expression_Matrix.rds")
lgg_expr <- readRDS("LGG_Expression_Matrix.rds")
lihc_expr <- readRDS("LIHC_Expression_Matrix.rds")

gbm_stem <- readRDS("GBM_Stemness_Vector.rds")
lgg_stem <- readRDS("LGG_Stemness_Vector.rds")
lihc_stem <- readRDS("LIHC_Stemness_Vector.rds")


# Combine expression matrices
combined_expr <- cbind(
  gbm_expr,
  lgg_expr,
  lihc_expr
)

# transpose:
samples_expr <- t(combined_expr)

write.csv(
  samples_expr,
  "pancancer_expression.csv"
)


metadata <- data.frame(
  sample=rownames(samples_expr),
  
  Cancer=c(
    rep("GBM",length(gbm_stem)),
    rep("LGG",length(lgg_stem)),
    rep("LIHC",length(lihc_stem))
  ),
  
  Stemness=c(
    gbm_stem,
    lgg_stem,
    lihc_stem
  )
)

write.csv(
  metadata,
  "pancancer_metadata.csv",
  row.names=FALSE
)
