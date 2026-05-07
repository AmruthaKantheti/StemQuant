#LOADING OF LOWER GRADE GLIOMA Expression
rm(list = ls())
gc()
list.files()
library(data.table)
library(GSVA)

# Load LGG expression
expr_lgg <- fread("TCGA_LGG_HiSeqV2")

expr_lgg <- as.data.frame(expr_lgg)

# First column is gene names
rownames(expr_lgg) <- expr_lgg[,1]
expr_lgg <- expr_lgg[,-1]

dim(expr_lgg)

#Conformation of gene names
head(rownames(expr_lgg))

#------stemness scoring----
#Loading of gene_set of ESC_stemness_signature
stem_genes = readLines("ESC_stemness_signature.txt")
gene_set = list(Stemness = stem_genes)  
                
length(gene_set[[1]])

library(GSVA)

ssgsea_param_lgg <- GSVA::ssgseaParam(
  expr = as.matrix(expr_lgg),
  geneSets = gene_set
)

stemness_lgg <- GSVA::gsva(ssgsea_param_lgg)

stemness_vector_lgg <- as.numeric(stemness_lgg[1, ])
names(stemness_vector_lgg) <- colnames(expr_lgg)

summary(stemness_vector_lgg)

saveRDS(stemness_vector_lgg, "LGG_Stemness_Vector.rds")

saveRDS(expr_lgg, "LGG_Expression_Matrix.rds")
