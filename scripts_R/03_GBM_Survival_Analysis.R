#GBM SURVIVAL ANALYIS
rm(list = ls())
gc()

#Loading of libraries
library(survival)
library(survminer)
library(data.table)

#STEP-1: Loading stemness data
stemness_vector = readRDS("GBM_Stemness_Vector.rds")
stem_group = readRDS("GBM_Stemness_Group.rds")

length(stemness_vector)
table(stem_group)

#STEP-2: Downloading clinical Data from Xena
#From XENA browser

#STEP-3: Laoding Clinical Data

clinical = fread("TCGA.GBM.sampleMap_GBM_clinicalMatrix")

clinical = as.data.frame(clinical)

dim(clinical)
head(clinical[,1:5])

#For identification of Survival columns

colnames(clinical)

#--------phase 2--------
#Creating survival variables
#conversion of column names to numeric

clinical$days_to_death <- as.numeric(clinical$days_to_death)
clinical$days_to_last_followup <- as.numeric(clinical$days_to_last_followup)

#Defining survival time
#In this code if the patient is dead using days_to_death
#If alive using days_to_last_followup
clinical$OS_time <- ifelse(
  !is.na(clinical$days_to_death),
  clinical$days_to_death,
  clinical$days_to_last_followup
)

#Cleaning vital_status
clinical$vital_status[clinical$vital_status == ""] <- NA

#Event: 1=dead, 0=alive
clinical$OS_event <- ifelse(
  clinical$vital_status == "DECEASED",
  1,
  0
)


table(clinical$OS_event)

table(clinical$vital_status)
table(clinical$CDE_vital_status)

#Recreating OS_time after changes

clinical$OS_time <- ifelse(
  clinical$vital_status == "DECEASED",
  clinical$days_to_death,
  clinical$days_to_last_followup
)

summary(clinical$OS_time)

#Removing Pateints with missing Survival
clinical <- clinical[!is.na(clinical$OS_time), ]

summary(clinical$OS_time)

#-------PHASE 3--------
#Step-1: Intersection with expression samples(172 samples)
common_samples <- intersect(
  names(stemness_vector),
  clinical$sampleID
)

length(common_samples)

#Creating Subset Stemness to common samples
#For the sample size 165
stemness_vector_sub <- stemness_vector[common_samples]
stem_group_sub <- stem_group[common_samples]

#Aligning Clinical with Expression order
clinical_sub <- clinical[clinical$sampleID %in% common_samples, ]

#Reorder clinical to match stemness order
clinical_sub <- clinical_sub[
  match(common_samples, clinical_sub$sampleID),
]

all(clinical_sub$sampleID == names(stemness_vector_sub))

#Adding stemness_group column
clinical_sub$Stemness_Group <- stem_group_sub
clinical_sub$Stemness_Score <- stemness_vector_sub
#Checking for column names
colnames(clinical_sub)
#Factor for Survival modeling

clinical_sub$Stemness_Group <- as.factor(clinical_sub$Stemness_Group)

table(clinical_sub$Stemness_Group)
#---------Kaplan-Meier Survival Analysis------

surv_object = Surv(
  time = clinical_sub$OS_time,
  event = clinical_sub$OS_event
)

fit = survfit(
  surv_object ~ Stemness_Group,
  data = clinical_sub
)

ggsurvplot(
  fit,
  data = clinical_sub,
  pval = TRUE,
  risk.table = TRUE,
  conf.int = TRUE,
  legend.title = "Stemness",
  legend.labs = c("High", "Low")
)

#Cox Proportional Hazards Model

cox_model = coxph(
  Surv(OS_time, OS_event) ~ Stemness_Score,
  data = clinical_sub
)

summary(cox_model)

#Forest plot for Cox Model
ggforest(cox_model, data = clinical_sub)

#Survival Curve using Continuous score
ggforest(cox_model, data = clinical_sub)

#Tertile based survival
clinical_sub$Stemness_Tertile <- cut(
  clinical_sub$Stemness_Score,
  breaks = quantile(clinical_sub$Stemness_Score, probs = c(0, 0.33, 0.66, 1)),
  include.lowest = TRUE,
  labels = c("Low", "Medium", "High")
)

fit_tertile <- survfit(
  Surv(OS_time, OS_event) ~ Stemness_Tertile,
  data = clinical_sub
)

ggsurvplot(
  fit_tertile,
  data = clinical_sub,
  pval = TRUE,
  risk.table = TRUE
)
