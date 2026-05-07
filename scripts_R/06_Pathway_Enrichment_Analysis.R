install.packages("BiocManager")
BiocManager::install("clusterProfiler")
BiocManager::install("enrichplot")
#Loading packages
library(clusterProfiler)
library(org.Hs.eg.db)
library(enrichplot)
library(ggplot2)

sessionInfo()

#Loading of Differential Expression results
deg_results = read.csv("LGG_Stemness_DEG_results.csv")
head(deg_results)

#Selection of significant genes
sig_genes <- deg_results[
  deg_results$adj.P.Val < 0.05 &
    abs(deg_results$logFC) > 1,
]

gene_symbols <- unique(
  sig_genes$Gene
)

length(gene_symbols)

#Conversion Gene symbols -> Entrez IDs
gene_entrez <- bitr(
  gene_symbols,
  fromType = "SYMBOL",
  toType = "ENTREZID",
  OrgDb = org.Hs.eg.db
)

head(gene_entrez)

#------GO Enrichment-----
GO_results <- enrichGO(
  gene = gene_entrez$ENTREZID,
  OrgDb = org.Hs.eg.db,
  ont = "BP",
  pAdjustMethod = "BH",
  pvalueCutoff = 0.05
)

head(
  as.data.frame(GO_results)
)

#Visualizing GO Pathways
GO_plot <- dotplot(
  GO_results,
  showCategory = 15
) +
  ggtitle("GO Biological Processes Associated with Tumor Stemness") +
  theme_bw() +
  theme(
    axis.text.y = element_text(size = 10),
    plot.title = element_text(hjust = 0.5, size = 14)
  )
GO_plot

library(stringr)

p_go <- dotplot(
  GO_results,
  showCategory=12,
  font.size=12
)+
  
  scale_y_discrete(
    labels=function(x)
      str_wrap(
        x,
        35
      )
  )+
  
  theme_classic(
    base_size=14
  )+
  
  labs(
    title=
      "GO Biological Processes Associated with Tumor Stemness"
  )+
  
  theme(
    plot.title=
      element_text(
        face="bold",
        hjust=.5
      ),
    
    axis.text.y=
      element_text(
        size=11
      ),
    
    legend.title=
      element_text(
        face="bold"
      )
  )

print(
  p_go
)

ggsave(
  "GO_Stemness_Pathways_Refined.tiff",
  p_go,
  width=9,
  height=7,
  dpi=600,
  compression="lzw"
)

#-------KEGG PATHWAY ANALYSIS-----
kegg_results <- enrichKEGG(
  gene = gene_entrez$ENTREZID,
  organism = "hsa",
  pvalueCutoff = 0.05
)

kegg_plot <- dotplot(kegg_results, showCategory = 15) +
  ggtitle("KEGG Pathways Associated with Tumor Stemness")

kegg_plot

#Saving the kegg plot
ggsave(
  "KEGG_Stemness_Pathways.png",
  kegg_plot,
  width = 8,
  height = 6,
  dpi = 300
)

#----stemness score distribution----
ggplot(data.frame(Stemness = stemness_vector_lgg),
       aes(x = Stemness)) +
  geom_histogram(fill = "#4DBBD5", bins = 40) +
  theme_bw() +
  labs(
    title = "Distribution of Stemness Scores in TCGA LGG",
    x = "Stemness Score",
    y = "Number of Tumors"
  )

ggsave("Stemness_Distribution_LGG.png", width=7, height=5)

save.image("Stemness_Project_Workspace.RData")
