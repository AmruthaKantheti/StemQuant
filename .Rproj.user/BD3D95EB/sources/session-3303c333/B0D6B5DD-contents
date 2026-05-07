#LOADING OF REQUIRED LIBRARIES
library(data.table)
library(GSVA)
library(survival)
library(survminer)

#Checking files
list.files(pattern = "LIHC")

#LOADING OF EXPRESSION DATA
expr_lihc_raw <- fread("TCGA_LIHC_HiSeqV2.txt")
dim(expr_lihc_raw)
head(expr_lihc_raw[,1:5])

#CONVERTING TO MATRIX FORMAT
expr_lihc <- as.data.frame(expr_lihc_raw)
#set gene names
rownames(expr_lihc) = expr_lihc[,1]
#Removing Gene column
expr_lihc = expr_lihc[,-1]

#REMOVING DUPLICATE GENES
expr_lihc <- expr_lihc[!duplicated(rownames(expr_lihc)), ]

#Converting to numeric matrix
expr_lihc <- as.matrix(expr_lihc)
mode(expr_lihc) <- "numeric"

#SAVING EXPRESSION MATRIX
saveRDS(expr_lihc, "LIHC_Expression_Matrix.rds")

#LOADING OF GENE SIGNATURE(STEMNESS)
gene_set = readLines("ESC_stemness_signature.txt")
gene_set = list(Stemness = gene_set)

#Computing stemness
stemness_score_lihc <- GSVA::gsva(
  GSVA::ssgseaParam(
    exprData = as.matrix(expr_lihc),
    geneSets = gene_set
  )
)

stemness_vector_lihc <- as.numeric(stemness_score_lihc[1,])
names(stemness_vector_lihc) <- colnames(expr_lihc)

summary(stemness_vector_lihc)
length(stemness_vector_lihc)

saveRDS(stemness_vector_lihc, "LIHC_Stemness_Vector.rds")

#LOADING OF SURVIVAL DATA
clinical_lihc <- fread("LIHC_survival.txt")
clinical_lihc <- as.data.frame(clinical_lihc)

head(clinical_lihc)
colnames(clinical_lihc)

#MATCHING OF SAMPLES
common_samples <- intersect(
  names(stemness_vector_lihc),
  clinical_lihc$sample
)
length(common_samples)

clinical_lihc <- clinical_lihc[
  clinical_lihc$sample %in% common_samples,
]

clinical_lihc <- clinical_lihc[
  match(common_samples, clinical_lihc$sample),
]

stemness_vector_lihc <- stemness_vector_lihc[common_samples]

#CREATING STEMNESS GROUPS
median_score <- median(stemness_vector_lihc)
clinical_lihc$Stemness_Group <- ifelse(
  stemness_vector_lihc >= median_score,
  "High",
  "Low"
)

table(clinical_lihc$Stemness_Group)

#-----phase-2------
library(survival)
library(survminer)

clinical_lihc$OS_months <- clinical_lihc$OS.time / 30
surv_object <- Surv(
  clinical_lihc$OS_months,
  clinical_lihc$OS
)

fit_lihc <- survfit(
  Surv(OS_months, OS) ~ Stemness_Group,
  data = clinical_lihc
)

plot_lihc <- ggsurvplot(
  fit_lihc,
  data = clinical_lihc,
  
  pval = TRUE,
  conf.int = FALSE,
  
  risk.table = TRUE,
  risk.table.height = 0.25,
  
  palette = c("#D55E00", "#0072B2"),
  
  legend.title = "Stemness",
  legend.labs = c("High", "Low"),
  
  xlab = "Time (months)",
  ylab = "Overall Survival Probability",
  
  title = "TCGA LIHC: Stemness Predicts Patient Survival",
  
  ggtheme = theme_bw(base_size = 14)
)

plot_lihc

#SAVING KM PLOT
ggsave(
  "LIHC_KM_Plot.png",
  plot_lihc$plot,
  width = 8,
  height = 6,
  dpi = 600
)

#COX PLOT
############################################################
# COX PROPORTIONAL HAZARDS MODEL
############################################################

library(survival)
library(ggplot2)

clinical_lihc$Stemness_Score <- stemness_vector_lihc

cox_lihc <- coxph(
  Surv(OS_months, OS) ~ stemness_vector_lihc,
  data=clinical_lihc
)

summary(cox_lihc)

############################################################
# EXTRACT MODEL STATISTICS
############################################################

hr <- exp(coef(cox_lihc))[1]

ci <- exp(
  confint(cox_lihc)
)

lower_ci <- ci[1]
upper_ci <- ci[2]

pval <- summary(
  cox_lihc
)$coefficients[5]

############################################################
# PUBLICATION STYLE FOREST PLOT
############################################################

cox_df <- data.frame(
  Variable="Stemness Score",
  HR=hr,
  Lower=lower_ci,
  Upper=upper_ci
)

p_cox <- ggplot(
  cox_df,
  aes(
    y=Variable,
    x=HR
  )
)+
  
  geom_errorbarh(
    aes(
      xmin=Lower,
      xmax=Upper
    ),
    height=.15,
    linewidth=1
  )+
  
  geom_point(
    size=5,
    shape=15
  )+
  
  geom_vline(
    xintercept=1,
    linetype="dashed"
  )+
  
  annotate(
    "text",
    x=12,
    y=1.28,
    
    label=
      paste0(
        "HR=",
        round(hr,2),
        "\n95% CI: ",
        round(lower_ci,2),
        "-",
        round(upper_ci,2),
        "\np<0.001"
      ),
    
    size=5
  )+
  
  scale_x_log10(
    breaks=c(
      1,
      2,
      5,
      10,
      20
    )
  )+
  
  theme_classic(
    base_size=16
  )+
  
  labs(
    title=
      "Cox Proportional Hazards Model for Stemness (TCGA LIHC)",
    
    x=
      "Hazard Ratio (log scale)",
    
    y=NULL
  )+
  
  theme(
    plot.title=
      element_text(
        face="bold",
        hjust=.5
      ),
    
    axis.text.y=
      element_text(
        face="bold",
        size=14
      ),
    
    axis.title.x=
      element_text(
        face="bold"
      )
  )

print(
  p_cox
)

############################################################
# SAVE PUBLICATION-QUALITY FIGURE
############################################################

ggsave(
  "LIHC_Cox_Publication_Refined.tiff",
  plot=p_cox,
  width=8,
  height=4.5,
  dpi=600,
  compression="lzw"
)
