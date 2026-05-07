#BIOLOGICAL VALIDATION
library(data.table)
library(ggplot2)

list.files()
#Expression matrix loading
expr_lgg <- readRDS("LGG_Expression_Matrix.rds")
stemness_vector_lgg = readRDS("LGG_Stemness_Vector.rds")

#Verification of Dimensions
dim(expr_lgg)
length(stemness_vector_lgg)

#Defining of stemness marker genes
stem_markers = c("SOX2", "PROM1", "NANOG", "POU5F1")
stem_markers %in% rownames(expr_lgg)

#-----CORRELATION ANALYSIS------
cor_results <- data.frame()

for(g in stem_markers){
  
  gene_exp <- as.numeric(expr_lgg[g,])
  
  cor_test <- cor.test(
    gene_exp,
    stemness_vector_lgg,
    method="spearman"
  )
  
  cor_results <- rbind(
    cor_results,
    data.frame(
      Gene = g,
      Correlation = cor_test$estimate,
      Pvalue = cor_test$p.value
    )
  )
}
rownames(cor_results) <- NULL
cor_results

#Saving the results
write.csv(
  cor_results,
  "Stemness_marker_correlation_LGG.csv",
  row.names = FALSE
)

############################################################
# STEMNESS VS TUMOR GRADE (LGG)
############################################################

library(ggplot2)
library(ggpubr)

############################################################
# CHECK AVAILABLE GRADE COLUMN
############################################################

colnames(clinical_lgg)

# Replace "tumor_grade" if your column name differs
# often "grade"
library(TCGAbiolinks)

clinical_grade <- GDCquery_clinic(
  project="TCGA-LGG",
  type="clinical"
)

colnames(clinical_grade)

# usually pathologic_grade or tumor_grade
table(
  clinical_grade$tumor_grade
)

# MATCH SAMPLE IDS
####################################################

clinical_grade$sample <- substr(
  clinical_grade$submitter_id,
  1,
  12
)

lgg_ids <- substr(
  names(stemness_vector_lgg),
  1,
  12
)

common <- intersect(
  lgg_ids,
  clinical_grade$sample
)

grade_df <- data.frame(
  sample=common,
  Stemness=
    stemness_vector_lgg[
      match(
        common,
        lgg_ids
      )
    ],
  Grade=
    clinical_grade$tumor_grade[
      match(
        common,
        clinical_grade$sample
      )
    ]
)

grade_df <- subset(
  grade_df,
  Grade %in% c(
    "G2",
    "G3"
  )
)

############################################################
# KRUSKAL-WALLIS TEST
############################################################

kruskal.test(
  Stemness ~ Grade,
  data=grade_df
)

############################################################
# PUBLICATION STYLE BOXPLOT
############################################################

p_grade <- ggplot(
  grade_df,
  aes(
    x=Grade,
    y=Stemness,
    fill=Grade
  )
)+
  
  geom_boxplot(
    width=.6,
    outlier.shape=16
  )+
  
  geom_jitter(
    width=.12,
    alpha=.4
  )+
  
  stat_compare_means(
    method="kruskal.test",
    label.y=max(
      grade_df$Stemness
    )+0.05
  )+
  
  theme_classic(
    base_size=15
  )+
  
  labs(
    title=
      "Stemness Score Across Tumour Grades (LGG)",
    
    x=
      "Tumour Grade",
    
    y=
      "Stemness Score"
  )+
  
  theme(
    plot.title=
      element_text(
        face="bold",
        hjust=.5
      ),
    
    legend.position="none"
  )

print(
  p_grade
)

############################################################
# SAVE FIGURE
############################################################

ggsave(
  "LGG_Stemness_vs_TumorGrade.tiff",
  plot=p_grade,
  width=6,
  height=5,
  dpi=600,
  compression="lzw"
)
