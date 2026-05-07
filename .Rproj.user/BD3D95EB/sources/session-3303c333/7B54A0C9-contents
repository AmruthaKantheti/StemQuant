#Loading the required data
library(limma)
library(ggplot2)

expr_lgg <- readRDS("LGG_Expression_Matrix.rds")
stemness_vector_lgg <- readRDS("LGG_Stemness_Vector.rds")

#Quick check
dim(expr_lgg)
length(stemness_vector_lgg)

#Creating Stemness groups
median_score <- median(stemness_vector_lgg)

stem_group <- ifelse(
  stemness_vector_lgg > median_score,
  "High",
  "Low"
)

table(stem_group)

#Preparing the Design Matrix
stem_group <- factor(stem_group, levels=c("Low","High"))

design <- model.matrix(~ stem_group)

head(design)

#Running The Differential Matrix
fit <- lmFit(expr_lgg, design)

fit <- eBayes(fit)

deg_results <- topTable(
  fit,
  coef = 2,
  number = Inf
)

head(deg_results)

#Addition of Gene Names
deg_results$Gene = rownames(deg_results)

#Saving the results
write.csv(
  deg_results,
  "LGG_Stemness_DEG_results.csv",
  row.names = FALSE
)

#-------VOLCANO PLOT-----
deg_results$Significance <- "NotSig"

deg_results$Significance[
  deg_results$adj.P.Val < 0.05 &
    abs(deg_results$logFC) > 1
] <- "Significant"

ggplot(deg_results,
       aes(x = logFC,
           y = -log10(adj.P.Val),
           color = Significance)) +
  
  geom_point(alpha = 0.6) +
  
  scale_color_manual(values=c("grey","red")) +
  
  theme_minimal() +
  
  labs(
    title="Differential Expression: High vs Low Stemness (LGG)",
    x="Log2 Fold Change",
    y="-log10 Adjusted P-value"
  )

#Saving the plot
ggsave(
  "LGG_Stemness_VolcanoPlot.png",
  width=7,
  height=6
)
