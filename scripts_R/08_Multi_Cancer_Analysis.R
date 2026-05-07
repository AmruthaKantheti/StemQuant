#CREATING SUMMARY TABLE
#STEP-1: Survival Impact
results <- data.frame(
  Cancer = c("GBM", "LGG", "LIHC"),
  HR = c(0.47, 0.6, 7.95),
  lower = c(0.18, 0.3, 2.3),
  upper = c(1.2, 1.1, 27.29),
  pvalue = c(0.1, 0.03, 0.001)
)

library(ggplot2)

p1 <- ggplot(results, aes(x=Cancer, y=HR)) +
  geom_point(size=4, color="#E64B35") +
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0.2) +
  geom_hline(yintercept=1, linetype="dashed") +
  scale_y_log10() +
  theme_classic(base_size = 14) +
  labs(
    title="Stemness Hazard Ratio Across Cancers",
    y="Hazard Ratio (log scale)",
    x="Cancer Type"
  ) +
  geom_text(
    aes(label = paste0("HR=", round(HR,2),
                       "\n p=", signif(pvalue,2))),
    vjust = -1,
    size = 4
  )

p1

#STEP-2:Stemness Distribution Across Cancers
stemness_vector_gbm  <- readRDS("GBM_Stemness_Vector.rds")
stemness_vector_lgg  <- readRDS("LGG_Stemness_Vector.rds")
stemness_vector_lihc <- readRDS("LIHC_Stemness_Vector.rds")

#COMBINING INTO ONE DATA FRAME
combined <- data.frame(
  Score = c(stemness_vector_gbm,
            stemness_vector_lgg,
            stemness_vector_lihc),
  
  Cancer = c(
    rep("GBM", length(stemness_vector_gbm)),
    rep("LGG", length(stemness_vector_lgg)),
    rep("LIHC", length(stemness_vector_lihc))
  )
)

#PLOT
library(ggplot2)

p2 <- ggplot(combined, aes(x=Cancer, y=Score, fill=Cancer)) +
  geom_boxplot(outlier.shape = NA, alpha=0.8) +
  geom_jitter(width=0.15, alpha=0.15, size=0.8) +
  
  theme_classic(base_size = 14) +
  
  labs(
    title="Stemness Score Distribution Across Cancer Types",
    x="Cancer Type",
    y="Stemness Score"
  ) +
  
  scale_fill_manual(values=c("#4DBBD5","#00A087","#E64B35")) +
  
  theme(
    legend.position="none",
    plot.title = element_text(hjust=0.5, face="bold")
  )

p2

#SAVING PLOT
ggsave("MULTI_CANCER_Stemness_Distribution.tiff",
       p2,
       width=7,
       height=5,
       dpi=600)

#Addition of p-values
library(ggpubr)

p2_final = p2 + stat_compare_means(
  comparisons = list(
    c("GBM","LGG"),
    c("GBM","LIHC"),
    c("LGG","LIHC")
  ),
  method = "wilcox.test"
)

p2_final
#Saving plot
ggsave(
  "MULTI_CANCER_Stemness_Dist_with_stats.tiff",
  plot = p2_final,
  width = 7,
  height = 5,
  dpi = 600
)

#PNG FORMAT
ggsave(
  "MULTI_CANCER_Stemness_Dist_with_stats.png",
  plot = p2_final,
  width = 7,
  height = 5,
  dpi = 300
)

#STEP-3: Statistical strength
results <- data.frame(
  Cancer = c("GBM", "LGG", "LIHC"),
  pvalue = c(0.13, 0.042, 0.001)
)
#Conversion to -log10 scale
results$logP <- -log10(results$pvalue)
results

#PLOT

library(ggplot2)

p3 <- ggplot(results, aes(x=Cancer, y=logP, fill=Cancer)) +
  geom_bar(stat="identity", width=0.6) +
  
  theme_classic(base_size = 14) +
  
  labs(
    title="Statistical Significance of Stemness Across Cancers",
    x="Cancer Type",
    y=expression(-log[10](p-value))
  ) +
  
  scale_fill_manual(values=c("#4DBBD5","#00A087","#E64B35")) +
  
  theme(
    legend.position="none",
    plot.title = element_text(hjust=0.5, face="bold")
  )

p3

#Adding p-values
p3_final <- p3 +
  geom_text(
    aes(label = paste0("p=", signif(pvalue,2))),
    vjust = -0.5,
    size = 4
  )

p3_final

#Saving the plot
ggsave(
  "Multi_cancer_Statistical_Significance.tiff",
  plot = p3_final,
  width = 7,
  height = 5,
  dpi = 600
)

#PNG FORMAT
ggsave(
  "Multi_cancer_Statistical_Significance.png",
  plot = p3_final,
  width = 7,
  height = 5,
  dpi = 300
)

#------pan cancer figure------
install.packages("patchwork")
library(patchwork)
#combining layout
combined_plot <- (p1 | p2_final) / p3_final
combined_plot
#Adding panel labels
combined_plot +
  plot_annotation(
    tag_levels = "A"
  )
#improve spacing
combined_plot <- (p1 | p2_final) /
  p3_final +
  plot_layout(heights = c(1, 1))

ggsave(
  "Final_PanCancer_Stemness_Figure.tiff",
  combined_plot,
  width = 12,
  height = 8,
  dpi = 600
)
