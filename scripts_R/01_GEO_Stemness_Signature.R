# Loading dataset
library(GEOquery)

gse <- getGEO("GSE12390", GSEMatrix = TRUE)
eset <- gse[[1]]

expr <- exprs(eset)
pdata <- pData(eset)
#Checking the matrix
dim(expr)

#Scan for title
table(pdata$source_name_ch1)

#Defining proper groups
group <- ifelse(
  grepl("embryonic stem|pluripotent", 
        pdata$source_name_ch1, ignore.case = TRUE),
  "Stem",
  "Differentiated"
)

group <- factor(group)
table(group)

#Confirming expression matrix

dim(expr)
class(expr[1,1])

#Differential expression 
library(limma)

design <- model.matrix(~ group)

fit <- lmFit(expr, design)
fit <- eBayes(fit)

deg <- topTable(
  fit,
  coef = 2,
  number = Inf,
  adjust.method = "BH"
)

head(deg)

#Extracting Stemness Genes
stemness_genes <- deg[
  deg$adj.P.Val < 0.01 & deg$logFC > 1,
]

nrow(stemness_genes)

#checking for rownames
head(rownames(expr))

#For mapping of probes
#Identifying platform
annotation(eset)

#installing platform annotation
#BiocManager::install("hgu133plus2.db")
library(hgu133plus2.db)

#Mapping probe id to gene symbols
library(AnnotationDbi)

gene_symbols <- mapIds(
  hgu133plus2.db,
  keys = rownames(expr),
  column = "SYMBOL",
  keytype = "PROBEID",
  multiVals = "first"
)
#Attaching gene symbols
expr_annot <- expr
expr_annot$GeneSymbol <- gene_symbols

# Remove probes without gene symbol
expr_annot <- expr_annot[!is.na(expr_annot$GeneSymbol), ]

#dimensional error
#so converting this matrix to dataframe
expr_df <- as.data.frame(expr)

#Now attaching gene symbols again
expr_df$GeneSymbol = gene_symbols

#No warnings
#Removing probes without Gene symbol
expr_df = expr_df[!is.na(expr_df$GeneSymbol), ]

#Keeping probe with highest average expression
#Collapse Multiple probes per gene

library(dplyr)
expr_collapsed = expr_df %>%
  group_by(GeneSymbol) %>%
  slice_max(order_by = rowMeans(across(where(is.numeric))), n=1) %>%
  ungroup()

#Converting back to matrix

expr_final <- as.matrix(expr_collapsed[, -which(colnames(expr_collapsed) == "GeneSymbol")])
rownames(expr_final) <- expr_collapsed$GeneSymbol

dim(expr_final)
head(rownames(expr_final))

#Final Differential expression(gene level)
library(limma)

design <- model.matrix(~ group)

fit <- lmFit(expr_final, design)
fit <- eBayes(fit)

deg <- topTable(
  fit,
  coef = 2,
  number = Inf,
  adjust.method = "BH"
)

head(deg)

#Exctracting stemness genes
stemness_genes <- deg[
  deg$adj.P.Val < 0.01 & deg$logFC > 1,
]

nrow(stemness_genes)


#Saving final stemness gene set
write.table(
  rownames(stemness_genes),
  file = "ESC_stemness_signature.txt",
  quote = FALSE,
  row.names = FALSE,
  col.names = FALSE
)

#checking whether pluripotency markers appear
rownames(stemness_genes)[1:50]
