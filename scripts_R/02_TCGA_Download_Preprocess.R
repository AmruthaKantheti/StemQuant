# 02_TCGA_DOWNLOAD_PREPROCESS
#if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

#BiocManager::install(c(
#  "TCGAbiolinks",
#  "SummarizedExperiment",
#  "GSVA",
#  "edgeR",
#  "limma",
#  "survival",
#  "survminer"
#))
#LOADING PACKAGES
library(TCGAbiolinks)
library(SummarizedExperiment)
library(GSVA)
library(limma)
library(org.Hs.eg.db)
library(AnnotationDbi)



#Deleting the incomplete files
unlink("GDCdata", recursive = TRUE)
unlink(list.files(pattern = "tar.gz"))

#TCGA GBM EXPRESSION LOADING
rm(list = ls())
gc()

library(data.table)
#Inspecting Raw file
raw_file <- fread("TCGA_GBM_HiSeqV2.txt")

class(raw_file)
dim(raw_file)
head(raw_file[, 1:5])

#Modification
#STEP-1: SETTING GENE NAMES AS ROWNAMES
expr_tcga <- as.data.frame(raw_file)
#Extracting frst column
gene_names <- expr_tcga[,1]
#Remove First column
expr_tcga <- expr_tcga[,-1]

#Assigning names
rownames(expr_tcga) <- gene_names

#Lets confirm the structure
dim(expr_tcga)
head(rownames(expr_tcga))

# ------PHASE 2 ------
#Loading ESC Stemness Gene signature

stem_genes <- scan("ESC_stemness_signature.txt", what = "character")
length(stem_genes)
head(stem_genes)

#Preparing for GSVA

gene_set = list(Stemness = stem_genes)

#Run GSVA(SSGSEA)

library(GSVA)

# Create GSVA parameter object
#Running GSVA and method is being specified

ssgsea_param <- GSVA::ssgseaParam(
  expr = as.matrix(expr_tcga),
  geneSets = gene_set
)

stemness_score = GSVA::gsva(ssgsea_param)

dim(stemness_score)

#Extraction of stemness vector
stemness_vector <- as.numeric(stemness_score[1, ])
names(stemness_vector) <- colnames(expr_tcga)

summary(stemness_vector)

#-----phase 3--------
#Creating High vs Low stemness score
#Splitting by Median as it is the Standard approach
median_score = median(stemness_vector)
stem_group = ifelse(
  stemness_vector >= median_score,
  "High",
  "Low"
)

table(stem_group)

#SAVING THE OUTPUT results
# Create data frame of results
stemness_df <- data.frame(
  Sample_ID = names(stemness_vector),
  Stemness_Score = stemness_vector,
  Stemness_Group = stem_group
)

#CSV for easy understanding
write.csv(
  stemness_df,
  file = "GBM_Stemness_Scores.csv",
  row.names = FALSE
)

# Saving R objects for future scripts
saveRDS(expr_tcga, "GBM_Expression_Matrix.rds")
saveRDS(stemness_vector, "GBM_Stemness_Vector.rds")
saveRDS(stem_group, "GBM_Stemness_Group.rds")

#Saving everything in One RDate file
save(expr_tcga, stemness_vector, stem_group,
     file = "GBM_Stemness_Workspace.RData")
