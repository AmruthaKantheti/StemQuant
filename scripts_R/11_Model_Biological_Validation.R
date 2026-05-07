############################################################
# Script 10
# MODEL BIOLOGICAL VALIDATION
############################################################

rm(list=ls())

############################################################
# LOAD LIBRARIES
############################################################

library(VennDiagram)
library(clusterProfiler)
library(org.Hs.eg.db)

############################################################
# TOP PREDICTIVE GENES FROM ML MODEL
############################################################

top_model_genes <- c(
  "FXYD6",
  "SCN3A",
  "DSCAM",
  "CEBPB",
  "ZNF711",
  "PTCHD2",
  "ABI2",
  "SBK1",
  "DPF1",
  "ZBTB7B",
  "NUDT11",
  "NLGN3",
  "TCF4",
  "KCNQ2",
  "STAT6"
)

############################################################
# LOAD STEMNESS SIGNATURE
############################################################
# Adjust filename if yours differs

stemness_signature <- readLines(
  "ESC_stemness_signature.txt"
)

############################################################
# OVERLAP WITH STEMNESS SIGNATURE
############################################################

overlap_sig <- intersect(
  top_model_genes,
  stemness_signature
)

cat(
  "\nOverlap with Stemness Signature:\n"
)

print(
  overlap_sig
)

cat(
  "\nNumber overlapping:",
  length(overlap_sig),
  "\n"
)

############################################################
# LOAD DIFFERENTIAL GENE RESULTS
############################################################

deg_results <- read.csv(
  "LGG_Stemness_DEG_results.csv",
  stringsAsFactors=FALSE
)

cat("\nDEG Columns:\n")
print(colnames(deg_results))

gene_col <- colnames(deg_results)[1]

deg_genes <- unique(
  deg_results[
    deg_results$adj.P.Val <0.05 &
      abs(deg_results$logFC)>1,
    gene_col
  ]
)

############################################################
# FILTER SIGNIFICANT DEGs
############################################################

deg_genes <- rownames(
  deg_results[
    deg_results$adj.P.Val <0.05 &
      abs(deg_results$logFC)>1,
  ]
)

############################################################
# OVERLAP WITH DEGs
############################################################

overlap_deg <- intersect(
  top_model_genes,
  deg_genes
)

print(
  overlap_deg
)

cat(
  "\nNumber overlapping:",
  length(overlap_deg),
  "\n"
)

############################################################
# VALIDATION TABLE
############################################################

validation_table <- data.frame(
  Gene=
    top_model_genes,
  
  In_Stemness_Signature=
    top_model_genes %in%
    stemness_signature,
  
  In_DEG=
    top_model_genes %in%
    deg_genes
)

print(
  validation_table
)

write.csv(
  validation_table,
  "Model_Gene_Validation.csv",
  row.names=FALSE
)

############################################################
# VENN DIAGRAM
############################################################

venn.diagram(
  list(
    ModelGenes=
      top_model_genes,
    
    StemnessSignature=
      stemness_signature
  ),
  
  filename=
    "Model_vs_Stemness_Venn.png",
  
  fill=c(
    "skyblue",
    "salmon"
  ),
  
  alpha=.5,
  
  cex=1.5
)

############################################################
# ENRICHMENT ON OVERLAPPING GENES
############################################################

overlap_genes <- top_model_genes

ego <- enrichGO(
  gene=overlap_genes,
  OrgDb=org.Hs.eg.db,
  keyType="SYMBOL",
  ont="BP"
)

head(as.data.frame(ego))

cat(
  "\nTop GO Terms:\n"
)

print(
  head(ego)
)

############################################################
# GO ENRICHMENT DOTPLOT
############################################################

pdf(
  "Predictive_Gene_GO_Enrichment.pdf",
  width=8,
  height=6
)

dotplot(
  ego,
  showCategory=10
)

dev.off()

############################################################
# SAVE ENRICHMENT RESULTS
############################################################

go_results <- as.data.frame(
  ego
)

write.csv(
  go_results,
  "Predictive_Gene_GO_Results.csv",
  row.names=FALSE
)

############################################################
# SUMMARY STATS
############################################################

overlap_percent <-
  length(overlap_sig)/
  length(top_model_genes)*100

cat(
  "\n======================================\n"
)

cat(
  "MODEL BIOLOGICAL VALIDATION COMPLETE\n"
)

cat(
  "\nSummary:\n"
)

cat(
  "Top predictive genes:",
  length(top_model_genes),"\n"
)

cat(
  "Overlap with stemness signature:",
  length(overlap_sig),"\n"
)

cat(
  "Overlap percentage:",
  round(overlap_percent,1),
  "%\n"
)

cat(
  "Overlap with DEGs:",
  length(overlap_deg),"\n"
)

cat(
  "\nOutputs generated:\n"
)

cat(
  "
Model_Gene_Validation.csv
Model_vs_Stemness_Venn.png
Predictive_Gene_GO_Enrichment.pdf
Predictive_Gene_GO_Results.csv
"
)

cat(
  "\n======================================\n"
)

list.files()
