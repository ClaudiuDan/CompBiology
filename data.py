data = {
        'gene_expr': {'hub': 'https://pancanatlas.xenahubs.net',
                        'cohort': 'TCGA Pan-Cancer (PANCAN)',
                        'dsets': ['TCGA-RPPA-pancan-clean.xena',
                                'Survival_SupplementalTable_S1_20171025_xena_sp',
                                'TCGA_phenotype_denseDataOnlyDownload.tsv'],
                        'target': 'cancer type abbreviation'},

        'gene_expr_dis': {'hub': 'https://pancanatlas.xenahubs.net',
                        'cohort': 'TCGA Pan-Cancer (PANCAN)',
                        'dsets': ['TCGA-RPPA-pancan-clean.xena',
                                'Survival_SupplementalTable_S1_20171025_xena_sp',
                                'TCGA_phenotype_denseDataOnlyDownload.tsv'],
                        'target': '_primary_disease'},
    
        'dna_metil': {'hub': 'https://pancanatlas.xenahubs.net',
                        'cohort': 'TCGA Pan-Cancer (PANCAN)',
                        'dsets': ['jhu-usc.edu_PANCAN_HumanMethylation450.betaValue_whitelisted.tsv.synapse_download_5096262.xena',
                                'TCGA_phenotype_denseDataOnlyDownload.tsv'],
                        'target': 'cancer type abbreviation'},

        'RNA_expr': {'hub': 'https://pancanatlas.xenahubs.net',
                        'cohort': 'TCGA Pan-Cancer (PANCAN)',
                        'dsets': ['EB++AdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.xena',
                                'Survival_SupplementalTable_S1_20171025_xena_sp'],
                        'target': 'cancer type abbreviation'},
        'RNA_expr_dis': {'hub': 'https://pancanatlas.xenahubs.net',
                        'cohort': 'TCGA Pan-Cancer (PANCAN)',
                        'dsets': ['EB++AdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.xena',
                                'Survival_SupplementalTable_S1_20171025_xena_sp',
                                'TCGA_phenotype_denseDataOnlyDownload.tsv'],
                        'target': '_primary_disease'}
}