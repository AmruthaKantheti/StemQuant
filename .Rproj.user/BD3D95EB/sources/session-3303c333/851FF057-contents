rm(list = ls())
gc()

library(survival)
library(survminer)
library(data.table)

#STEP-2: Loading of Stemness Vector
stemness_vector_lgg <- readRDS("LGG_Stemness_Vector.rds")
length(stemness_vector_lgg)

#STEP-3: Loading Clinical Data
list.files()
library(data.table)

clinical_lgg <- fread("survival_LGG_survival.txt")
clinical_lgg <- as.data.frame(clinical_lgg)

dim(clinical_lgg)
head(clinical_lgg)

colnames(clinical_lgg)

#--------PHASE-2---------
#STEP-1:Matching the expression with clinical
common_samples <- intersect(
  names(stemness_vector_lgg),
  clinical_lgg$sample
)

length(common_samples)

#STEP-2: Aligning of both datasets
stemness_vector_lgg <- stemness_vector_lgg[common_samples]

clinical_lgg <- clinical_lgg[
  clinical_lgg$sample %in% common_samples,
]

clinical_lgg <- clinical_lgg[
  match(common_samples, clinical_lgg$sample),
]

#STEP-3: Creating the Stemness Groups
median_lgg <- median(stemness_vector_lgg)

clinical_lgg$Stemness_Group <- ifelse(
  stemness_vector_lgg >= median_lgg,
  "High",
  "Low"
)

table(clinical_lgg$Stemness_Group)

#STEP-4: Kaplan-Meier Survival
library(survival)
library(survminer)
clinical_lgg$OS_months <- clinical_lgg$OS.time / 30.44

surv_object = Surv(
  clinical_lgg$OS_months,
  clinical_lgg$OS
)

fit_lgg = survfit(
  surv_object ~ Stemness_Group,
  data = clinical_lgg
)

#STEP-5: Survival Plot
#Publication style km plot
km_plot <- ggsurvplot(
  fit_lgg,
  data = clinical_lgg,
  pval = TRUE,
  risk.table = TRUE,
  conf.int = FALSE,
  palette = c("#E64B35", "#4DBBD5"),
  xlab = "Time (Months)",
  ylab = "Overall Survival Probability",
  title = "Stemness Score Predicts Survival in TCGA Lower Grade Glioma",
  break.time.by = 12,
  risk.table.height = 0.25,
  ggtheme = theme_bw(),
  legend.title = "Stemness",
  legend.labs = c("High", "Low")
)

km_plot

#SAVING THE FIGURE
ggsave(
  "LGG_Stemness_Survival.png",
  km_plot$plot,
  width = 8,
  height = 6,
  dpi = 300
)

#Cox Model
summary(clinical_lgg$OS_months)
cox_lgg <- coxph(
  Surv(OS_months, OS) ~ stemness_vector_lgg,
  data = clinical_lgg
)

summary(cox_lgg)

#Generating Forest(Cox) plot
library(survminer)

ggforest(
  cox_lgg,
  data = clinical_lgg,
  main = "Stemness Score Cox Regression - TCGA LGG"
)

#Saving the plot
ggsave(
  "LGG_Cox_Forest_Plot.png",
  width = 8,
  height = 6,
  dpi = 300
)

#Subtype and tumor grade analysis
#--------Additional phase------

#STEP-1: LOADING OF CLINICAL MATRIX

clinical_matrix <- fread("TCGA.LGG.sampleMap_LGG_clinicalMatrix")
clinical_matrix <- as.data.frame(clinical_matrix)

dim(clinical_matrix)

#STEP-2: KEEPING IMPORTANT AND REQUIRED COLUMNS

clinical_sub <- clinical_matrix[, c(
  "sampleID",
  "age_at_initial_pathologic_diagnosis",
  "gender",
  "histological_type",
  "neoplasm_histologic_grade",
  "karnofsky_performance_score",
  "vital_status",
  "days_to_death",
  "days_to_last_followup"
)]

head(clinical_sub)

#STEP-3:CREATING SURVIVAL VARIABLES

clinical_sub$days_to_death <- as.numeric(clinical_sub$days_to_death)
clinical_sub$days_to_last_followup <- as.numeric(clinical_sub$days_to_last_followup)

clinical_sub$OS_time <- ifelse(
  clinical_sub$vital_status == "DECEASED",
  clinical_sub$days_to_death,
  clinical_sub$days_to_last_followup
)

clinical_sub$OS_event <- ifelse(
  clinical_sub$vital_status == "DECEASED",1,0)

#STEP-4: MATCHING THE STEMNESS SCORE

common_samples <- intersect(
  names(stemness_vector_lgg),
  clinical_sub$sampleID
)

length(common_samples)

#ALIGNING OF SAMPLES

clinical_sub <- clinical_sub[
  clinical_sub$sampleID %in% common_samples,
]

clinical_sub <- clinical_sub[
  match(common_samples, clinical_sub$sampleID),
]

clinical_sub$Stemness_Score <- stemness_vector_lgg[common_samples]

clinical_sub <- clinical_sub[
  clinical_sub$neoplasm_histologic_grade %in% c("G2","G3"),
]
#STEP-5: STEMNESS VS TUMOR GRADE

library(ggplot2)

ggplot(clinical_sub,
       aes(x = neoplasm_histologic_grade,
           y = Stemness_Score,
           fill = neoplasm_histologic_grade)) +
  geom_boxplot() +
  theme_bw() +
  labs(
    title="Stemness Score Across Tumor Grades (TCGA LGG)",
    x="Tumor Grade",
    y="Stemness Score"
  ) +
  scale_fill_manual(values=c("#4DBBD5","#E64B35"))

#Saving the plot
ggsave(
  "LGG_Stemness_vs_TumorGrade.png",
  width = 7,
  height = 6,
  dpi = 300
)

#STATISTICAL TEST
# KRUSKAL TEST

kruskal.test(
  Stemness_Score ~ neoplasm_histologic_grade,
  data = clinical_sub
)

saveRDS(expr_lgg, "LGG_Expression_Matrix.rds")
