# 基于病原与宿主免疫转录组的感染判断建模与智能体分析解读：相关文献整理

> 检索日期：2026-09-09  
> 数据源：Europe PMC、PubMed 元数据与 Crossref  
> 收录数量：44 篇（43 篇同行评议论文，1 篇明确标注的预印本）

## 1. 检索范围与使用说明

本次检索围绕以下五条主线展开：

1. **宿主转录组感染判断**：感染/非感染、细菌/病毒、感染类型多分类和早期诊断。
2. **脓毒症与免疫内型**：感染性炎症与无菌性炎症区分、严重度预测、宿主反应异质性。
3. **病原无偏测序与宿主-病原联合诊断**：宏基因组/宏转录组、临床 mNGS、病原与宿主特征融合。
4. **双转录组与单细胞宿主-病原互作**：同时刻画病原表达状态和宿主免疫反应。
5. **智能体与基础模型**：工具增强的大语言模型、转录组基础模型、自动化单细胞分析和临床文本融合。

检索优先纳入具备下列价值的论文：多队列或外部验证、前瞻性临床验证、可复现方法、宿主与病原联合分析、经典方法学贡献，以及能支撑“智能体分析解读”模块设计的研究。植物/动物感染、纯肿瘤微生物组、只有会议摘要且缺少完整论文的记录未纳入。

**日期口径**：下文“发表日期”采用 Europe PMC 的 `firstPublicationDate`，通常对应首次在线发表日；它可能早于纸质卷期日期。DOI 不区分大小写，本文统一使用数据库返回形式。本文是面向课题设计的主题性文献整理，不等同于按 PRISMA 标准完成的系统综述；正式写入毕业论文前，仍应按学校格式逐条核对卷、期、页码和作者列表。

## 2. 优先阅读清单

如果时间有限，建议优先读以下 12 篇：

| 优先级 | 文献 | 直接用途 |
|---|---|---|
| 1 | Langelier et al., 2018, PNAS | 与课题最接近：在一次呼吸道样本测序中联合病原、微生物组和宿主转录特征 |
| 2 | Doxey et al., 2025, Genome Medicine | 鼻咽宏转录组同时完成病原检测和宿主细菌/病毒反应分析 |
| 3 | Mayhew et al., 2020, Nature Communications | 29-mRNA 神经网络与独立队列验证，可作为宿主模型基线 |
| 4 | Sweeney et al., 2016, Science Translational Medicine | 多队列整合、7 基因细菌/病毒签名与感染决策模型 |
| 5 | Bodkin et al., 2022, Genome Medicine | 统一比较 28 个已发表宿主签名，直接揭示泛化问题 |
| 6 | Schlapbach et al., 2024, Lancet Child & Adolescent Health | 同时预测感染类型与器官功能障碍，体现多任务建模思路 |
| 7 | Chiu & Miller, 2019, Nature Reviews Genetics | 临床 mNGS 的完整框架、实验与解释难点 |
| 8 | Westermann et al., 2016, Nature | 双 RNA-seq 关联病原调控因子与宿主通路的代表作 |
| 9 | Aprianto et al., 2016, Genome Biology | 时间分辨双 RNA-seq，适合借鉴动态特征和互作网络 |
| 10 | Phan et al., 2025, Nature Communications | 宿主转录标志物与 LLM 临床文本联合诊断的直接先例 |
| 11 | GeneGPT, 2024, Bioinformatics | 用数据库 API 约束 LLM，适合设计可追溯的证据型解释智能体 |
| 12 | CellAgent, 2024, bioRxiv（预印本） | 多智能体编排转录组分析流程，适合作为系统架构参考 |

## 3. 宿主转录组感染判断与机器学习

### H1. Gene expression signatures diagnose influenza and other symptomatic respiratory viral infections in humans

- **作者 / 期刊**：Zaas AK et al.; *Cell Host & Microbe*
- **发表日期**：2009-08-06
- **DOI**：[10.1016/j.chom.2009.07.006](https://doi.org/10.1016/j.chom.2009.07.006)
- **PMID**：[19664979](https://pubmed.ncbi.nlm.nih.gov/19664979/)
- **简单摘要**：利用鼻病毒、呼吸道合胞病毒和甲型流感病毒人体攻毒数据建立外周血表达签名。该签名区分有症状病毒感染与未感染者的准确率超过 95%，并在独立流感数据中验证，同时显示区分病毒与细菌性急性呼吸道感染的潜力。
- **课题价值**：这是“宿主表达可替代单纯病原检测进行感染判断”的早期关键证据，可用于绪论和研究假设。

### H2. A host transcriptional signature for presymptomatic detection of infection in humans exposed to influenza H1N1 or H3N2

- **作者 / 期刊**：Woods CW et al.; *PLOS ONE*
- **发表日期**：2013-01-09
- **DOI**：[10.1371/journal.pone.0052198](https://doi.org/10.1371/journal.pone.0052198)
- **PMID**：[23326326](https://pubmed.ncbi.nlm.nih.gov/23326326/)
- **简单摘要**：对 41 名接受 H1N1 或 H3N2 暴露的志愿者每 8 小时采集外周血转录组；18 人出现症状。所得宿主签名可识别 94% 的感染者，最早在暴露后 29 小时出现，并早于症状峰值约 38 至 43 小时。
- **课题价值**：提示模型可从“是否感染”扩展到“症状前预警”，但时间点相关偏移必须在验证方案中单独处理。

### H3. Superiority of transcriptional profiling over procalcitonin for distinguishing bacterial from viral lower respiratory tract infections in hospitalized adults

- **作者 / 期刊**：Suarez NM et al.; *The Journal of Infectious Diseases*
- **发表日期**：2015-01-29
- **DOI**：[10.1093/infdis/jiv047](https://doi.org/10.1093/infdis/jiv047)
- **PMID**：[25637350](https://pubmed.ncbi.nlm.nih.gov/25637350/)
- **简单摘要**：研究纳入 118 名住院下呼吸道感染患者和 40 名健康对照，发现细菌感染偏向炎症基因表达，病毒感染偏向干扰素相关表达。10 基因 KNN 分类器区分细菌和病毒感染的敏感度/特异度为 95%/92%，敏感度明显高于降钙素原。
- **课题价值**：适合用作与传统临床生物标志物对比的基准，并提示细菌-病毒混合感染应被单独建模。

### H4. Host gene expression classifiers diagnose acute respiratory illness etiology

- **作者 / 期刊**：Tsalik EL et al.; *Science Translational Medicine*
- **发表日期**：2016-01-01
- **DOI**：[10.1126/scitranslmed.aad6873](https://doi.org/10.1126/scitranslmed.aad6873)
- **PMID**：[26791949](https://pubmed.ncbi.nlm.nih.gov/26791949/)
- **简单摘要**：基于 273 名急性呼吸道疾病患者及 44 名健康对照的全血表达数据，分别构建细菌、病毒和非感染分类器，总体准确率为 87%。模型在 5 个公开数据集中获得 0.90 至 0.99 的 AUC，并能表现出细菌、病毒、混合感染及二者均无的四类宿主反应。
- **课题价值**：提供了层级/多标签感染判断思路，而不是强迫所有样本进入互斥二分类。

### H5. Robust classification of bacterial and viral infections via integrated host gene expression diagnostics

- **作者 / 期刊**：Sweeney TE et al.; *Science Translational Medicine*
- **发表日期**：2016-07-01
- **DOI**：[10.1126/scitranslmed.aaf7165](https://doi.org/10.1126/scitranslmed.aaf7165)
- **PMID**：[27384347](https://pubmed.ncbi.nlm.nih.gov/27384347/)
- **简单摘要**：通过多队列整合得到 7 基因细菌/病毒分类签名，并在 30 个独立队列中验证；再与 11 基因 Sepsis MetaScore 组合形成抗生素决策模型。在 20 个队列、1057 个样本的合并分析中，对细菌感染的敏感度为 94.0%，特异度为 59.8%。
- **课题价值**：高度适合借鉴其跨平台、多队列效应量整合及“先感染、再病原类别”的分层模型设计。

### H6. Diagnostic Test Accuracy of a 2-Transcript Host RNA Signature for Discriminating Bacterial vs Viral Infection in Febrile Children

- **作者 / 期刊**：Herberg JA et al.; *JAMA*
- **发表日期**：2016-08-01
- **DOI**：[10.1001/jama.2016.11236](https://doi.org/10.1001/jama.2016.11236)
- **PMID**：[27552617](https://pubmed.ncbi.nlm.nih.gov/27552617/)
- **简单摘要**：研究从儿童发热队列中将 38 转录本签名缩减为 FAM89A 与 IFI44L 两个转录本。在验证组中，对确证细菌感染的敏感度为 100%，对确证病毒感染的特异度为 96.4%，但作者强调仍需更广泛临床验证。
- **课题价值**：展示了从高维表达谱到极简可转化检测试剂的路径，也提醒小样本高指标可能存在不确定性。

### H7. Association of RNA Biosignatures With Bacterial Infections in Febrile Infants Aged 60 Days or Younger

- **作者 / 期刊**：Mahajan P et al.; *JAMA*
- **发表日期**：2016-08-01
- **DOI**：[10.1001/jama.2016.9207](https://doi.org/10.1001/jama.2016.9207)
- **PMID**：[27552618](https://pubmed.ncbi.nlm.nih.gov/27552618/)
- **简单摘要**：在 279 名 60 日龄以内发热婴儿中，66 基因签名区分有无细菌感染的敏感度/特异度为 87%/89%；10 基因签名识别菌血症的敏感度/特异度为 94%/95%。结果支持宿主 RNA 对培养法的补充价值。
- **课题价值**：可作为年龄特异性、低采血量和类别不平衡问题的临床案例。

### H8. A generalizable 29-mRNA neural-network classifier for acute bacterial and viral infections

- **作者 / 期刊**：Mayhew MB et al.; *Nature Communications*
- **发表日期**：2020-03-04
- **DOI**：[10.1038/s41467-020-14975-w](https://doi.org/10.1038/s41467-020-14975-w)
- **PMID**：[32132525](https://pubmed.ncbi.nlm.nih.gov/32132525/)
- **简单摘要**：用 18 项回顾性研究的 1069 个样本训练 29-mRNA 神经网络 IMX-BVN-1，训练数据中细菌和病毒任务 AUROC 均为 0.92。在独立 163 人队列中两项 AUROC 分别为 0.86 和 0.85，入院 36 小时内亚组提升至 0.92 和 0.91。
- **课题价值**：可作为神经网络宿主模型的核心复现基线，并用于讨论固定基因面板、独立验证和采样时机。

### H9. Systematic comparison of published host gene expression signatures for bacterial/viral discrimination

- **作者 / 期刊**：Bodkin N et al.; *Genome Medicine*
- **发表日期**：2022-02-21
- **DOI**：[10.1186/s13073-022-01025-x](https://doi.org/10.1186/s13073-022-01025-x)
- **PMID**：[35184750](https://pubmed.ncbi.nlm.nih.gov/35184750/)
- **简单摘要**：在 51 个公开数据集、4589 名受试者中统一验证 28 个已发表签名，并另外分析 13 个 COVID-19 数据集。不同签名的细菌分类中位 AUC 为 0.55 至 0.96、病毒分类为 0.69 至 0.97，性能明显受签名规模、年龄与感染类型影响。
- **课题价值**：这是设计严格基准实验、跨队列验证和亚组公平性分析的关键参考，能避免只在单一数据集报告高分。

### H10. Prospective Validation of a Rapid Host Gene Expression Test to Discriminate Bacterial From Viral Respiratory Infection

- **作者 / 期刊**：Ko ER et al.; *JAMA Network Open*
- **发表日期**：2022-04-01
- **DOI**：[10.1001/jamanetworkopen.2022.7299](https://doi.org/10.1001/jamanetworkopen.2022.7299)
- **PMID**：[35420659](https://pubmed.ncbi.nlm.nih.gov/35420659/)
- **简单摘要**：前瞻性多中心研究纳入 755 名儿童和成人，用约 45 分钟检测 45 个宿主 mRNA。在 334 名高置信度裁定病例中，细菌感染敏感度 89.8%、特异度 82.1%、阴性预测值 97.9%，总体优于降钙素原。
- **课题价值**：为模型临床终点、输出概率分层、周转时间和抗菌药物管理价值提供了成熟范例。

### H11. bvnGPS: a generalizable diagnostic model for acute bacterial and viral infection using integrative host transcriptomics and pretrained neural networks

- **作者 / 期刊**：Li Q et al.; *Bioinformatics*
- **发表日期**：2023-03-01
- **DOI**：[10.1093/bioinformatics/btad109](https://doi.org/10.1093/bioinformatics/btad109)
- **PMID**：[36857587](https://pubmed.ncbi.nlm.nih.gov/36857587/)
- **简单摘要**：整合 16 个队列共 2680 个样本，用基因对相对表达降低批次效应，再以多分类神经网络组合细菌、病毒和非感染签名。测试集细菌/病毒 AUC 分别为 0.953/0.956，独立验证集分别为 0.988/0.994，并公开了代码。
- **课题价值**：非常适合作为跨平台归一化和多分类建模参考；复现时应特别审计队列划分与特征选择是否完全在训练折内完成。

### H12. Diagnosis of childhood febrile illness using a multi-class blood RNA molecular signature

- **作者 / 期刊**：Habgood-Coote D et al.; *Med*
- **发表日期**：2023-08-18
- **DOI**：[10.1016/j.medj.2023.06.007](https://doi.org/10.1016/j.medj.2023.06.007)
- **PMID**：[37597512](https://pubmed.ncbi.nlm.nih.gov/37597512/)
- **简单摘要**：在 12 个公开数据集的 1212 名儿童、18 类感染或炎症性疾病上进行带误诊代价权重的多分类学习，获得 161 转录本面板，并在 411 名发热儿童 RNA-seq 队列中验证。模型既能输出具体疾病，也能输出细菌、病毒、疟疾、结核和炎症等大类。
- **课题价值**：适合借鉴成本敏感学习与层级标签设计，使模型输出更贴近临床决策代价。

## 4. 脓毒症、感染性炎症与宿主免疫内型

### S1. A comprehensive time-course-based multicohort analysis of sepsis and sterile inflammation reveals a robust diagnostic gene set

- **作者 / 期刊**：Sweeney TE et al.; *Science Translational Medicine*
- **发表日期**：2015-05-01
- **DOI**：[10.1126/scitranslmed.aaa5993](https://doi.org/10.1126/scitranslmed.aaa5993)
- **PMID**：[25972003](https://pubmed.ncbi.nlm.nih.gov/25972003/)
- **简单摘要**：从 27 个脓毒症表达数据集中筛得 5 个包含感染与时间匹配无菌炎症的发现队列，采用留一数据集法获得 11 基因 Sepsis MetaScore，并在 15 个独立队列中验证。该签名可较稳健地区分感染性和无菌性系统炎症。
- **课题价值**：强调“感染 vs 非感染炎症”必须优先于“细菌 vs 病毒”，并给出跨研究效应量整合范式。

### S2. A Molecular Host Response Assay to Discriminate Between Sepsis and Infection-Negative Systemic Inflammation in Critically Ill Patients: Discovery and Validation in Independent Cohorts

- **作者 / 期刊**：McHugh L et al.; *PLOS Medicine*
- **发表日期**：2015-12-08
- **DOI**：[10.1371/journal.pmed.1001916](https://doi.org/10.1371/journal.pmed.1001916)
- **PMID**：[26645559](https://pubmed.ncbi.nlm.nih.gov/26645559/)
- **简单摘要**：发现 CEACAM4、LAMP1、PLA2G7 和 PLAC8 四基因分类器 SeptiCyte Lab，并在荷兰 5 个独立队列中用 RT-qPCR 验证。明确病例队列 AUC 为 0.95，更异质的验证病例 AUC 为 0.89，且疾病严重度并非主要混杂因素。
- **课题价值**：展示从转录组发现到小面板分子检测的临床转化路径，同时揭示“脓毒症缺少绝对金标准”的标签难题。

### S3. Genomic landscape of the individual host response and outcomes in sepsis: a prospective cohort study

- **作者 / 期刊**：Davenport EE et al.; *The Lancet Respiratory Medicine*
- **发表日期**：2016-02-23
- **DOI**：[10.1016/s2213-2600(16)00046-1](https://doi.org/10.1016/s2213-2600(16)00046-1)
- **PMID**：[26917434](https://pubmed.ncbi.nlm.nih.gov/26917434/)
- **简单摘要**：对社区获得性肺炎脓毒症患者外周血白细胞进行转录组分析，识别 SRS1 和 SRS2 两种宿主反应状态。SRS1 呈内毒素耐受、T 细胞耗竭和 HLA-II 下调等免疫抑制特征，并与更高 14 日死亡风险相关；7 基因可区分两型。
- **课题价值**：说明感染判断之外还应评估宿主免疫状态与预后，且同一种感染标签内部存在显著异质性。

### S4. Classification of patients with sepsis according to blood genomic endotype: a prospective cohort study

- **作者 / 期刊**：Scicluna BP et al.; *The Lancet Respiratory Medicine*
- **发表日期**：2017-08-29
- **DOI**：[10.1016/s2213-2600(17)30294-1](https://doi.org/10.1016/s2213-2600(17)30294-1)
- **PMID**：[28864056](https://pubmed.ncbi.nlm.nih.gov/28864056/)
- **简单摘要**：在多个 ICU 前瞻性队列中通过无监督聚类识别 Mars1 至 Mars4 四种脓毒症分子内型。Mars1 在各队列中稳定关联较高 28 日死亡率，并以免疫抑制特征为主；140 基因签名及 BPGM/TAP2 候选标志物可辅助内型识别。
- **课题价值**：可指导模型采用“诊断 + 内型 + 严重度”的多任务输出，而不是只给单一感染概率。

### S5. Unsupervised Analysis of Transcriptomics in Bacterial Sepsis Across Multiple Datasets Reveals Three Robust Clusters

- **作者 / 期刊**：Sweeney TE et al.; *Critical Care Medicine*
- **发表日期**：2018-06-01
- **DOI**：[10.1097/ccm.0000000000003084](https://doi.org/10.1097/ccm.0000000000003084)
- **PMID**：[29537985](https://pubmed.ncbi.nlm.nih.gov/29537985/)
- **简单摘要**：整合 14 个数据集、700 名细菌性脓毒症患者，得到 Inflammopathic、Adaptive 和 Coagulopathic 三类分子亚型，并在 9 个独立数据集、600 人中验证。Adaptive 型严重度和死亡率较低，Coagulopathic 型死亡率和凝血异常更高。
- **课题价值**：为跨队列无监督亚型发现、聚类稳定性和亚型生物学解释提供方法参考。

### S6. Predicting sepsis severity at first clinical presentation: The role of endotypes and mechanistic signatures

- **作者 / 期刊**：Baghela A et al.; *EBioMedicine*
- **发表日期**：2022-01-10
- **DOI**：[10.1016/j.ebiom.2021.103776](https://doi.org/10.1016/j.ebiom.2021.103776)
- **PMID**：[35027333](https://pubmed.ncbi.nlm.nih.gov/35027333/)
- **简单摘要**：分析 348 名急诊/ICU 患者及 44 名健康对照的血液 RNA-seq，严重度和死亡预测 AUC/准确率约为 77% 至 80%。研究进一步识别五种机制内型，并建立 40 基因内型分类器，在验证队列中准确率达 96%。
- **课题价值**：适合借鉴机制驱动的内型命名、通路解释和早期风险分层方案。

### S7. Host gene expression signatures to identify infection type and organ dysfunction in children evaluated for sepsis: a multicentre cohort study

- **作者 / 期刊**：Schlapbach LJ et al.; *The Lancet Child & Adolescent Health*
- **发表日期**：2024-03-19
- **DOI**：[10.1016/s2352-4642(24)00017-8](https://doi.org/10.1016/s2352-4642(24)00017-8)
- **PMID**：[38513681](https://pubmed.ncbi.nlm.nih.gov/38513681/)
- **简单摘要**：在儿童疑似脓毒症队列中分别构建 10 基因感染类别签名和 10 基因器官功能障碍签名；内部验证 AUC 分别为 0.941 和 0.822。两签名串联后对细菌或病毒感染背景下器官功能障碍有较高 AUC，但外部 EUCLIDS 队列表现下降至约 0.70。
- **课题价值**：同时证明多任务建模价值和外部泛化风险；文中内外部性能落差尤其值得在论文讨论中分析。

## 5. 病原宏转录组、临床无偏测序与联合诊断

> 本节包含若干以 DNA/RNA 临床 mNGS 为核心的论文。它们不全是严格意义上的“病原转录组”，但对病原读段过滤、污染背景建模、阈值设定、实验质控和临床解释具有直接方法学价值。

### P1. Rapid metagenomic identification of viral pathogens in clinical samples by real-time nanopore sequencing analysis

- **作者 / 期刊**：Greninger AL et al.; *Genome Medicine*
- **发表日期**：2015-09-29
- **DOI**：[10.1186/s13073-015-0220-9](https://doi.org/10.1186/s13073-015-0220-9)
- **PMID**：[26416663](https://pubmed.ncbi.nlm.nih.gov/26416663/)
- **简单摘要**：将 MinION 纳米孔测序与实时分析流程 MetaPORE 结合，在血液样本中无偏检出基孔肯雅、埃博拉和丙肝病毒。高滴度病毒可在开始采集后 4 至 10 分钟发现，整体样本到结果时间低于 6 小时。
- **课题价值**：可支撑流式数据、实时病原告警和快速报告模块设计，但低丰度样本仍是主要困难。

### P2. Clinical Metagenomic Next-Generation Sequencing for Pathogen Detection

- **作者 / 期刊**：Gu W et al.; *Annual Review of Pathology*
- **发表日期**：2018-10-24
- **DOI**：[10.1146/annurev-pathmechdis-012418-012751](https://doi.org/10.1146/annurev-pathmechdis-012418-012751)
- **PMID**：[30355154](https://pubmed.ncbi.nlm.nih.gov/30355154/)
- **研究类型**：综述
- **简单摘要**：系统介绍无靶向 mNGS 的测序平台、临床实验流程、生物信息分析、性能验证以及典型应用案例，重点讨论传统病原检测受限场景中的优势与障碍。
- **课题价值**：适合用作病原侧技术路线总览，并据此设计阴性对照、背景污染模型和正交验证。

### P3. Integrating host response and unbiased microbe detection for lower respiratory tract infection diagnosis in critically ill adults

- **作者 / 期刊**：Langelier C et al.; *Proceedings of the National Academy of Sciences (PNAS)*
- **发表日期**：2018-11-27
- **DOI**：[10.1073/pnas.1809700115](https://doi.org/10.1073/pnas.1809700115)
- **PMID**：[30482864](https://pubmed.ncbi.nlm.nih.gov/30482864/)
- **简单摘要**：对 92 名急性呼吸衰竭成人的气管吸出物进行 mNGS，在同一流程中评估病原体、气道微生物组和宿主转录组。验证队列中病原指标、微生物多样性指标和宿主分类器 AUC 分别为 0.96、0.80 和 0.88，联合后阴性预测值达到 100%。
- **课题价值**：是本课题最直接的技术先例，可把模型设计成病原证据、生态失衡和宿主免疫三分支后融合。

### P4. Laboratory validation of a clinical metagenomic sequencing assay for pathogen detection in cerebrospinal fluid

- **作者 / 期刊**：Miller S et al.; *Genome Research*
- **发表日期**：2019-04-16
- **DOI**：[10.1101/gr.238170.118](https://doi.org/10.1101/gr.238170.118)
- **PMID**：[30992304](https://pubmed.ncbi.nlm.nih.gov/30992304/)
- **简单摘要**：在持证临床实验室中验证脑脊液泛病原 mNGS 和 SURPI+ 分析流程，建立质量指标、阈值和检出限。盲测 95 份样本时初始敏感度 73%、特异度 99%；前瞻性挑战样本中相对常规检测的敏感度/特异度为 92%/96%。
- **课题价值**：提供从研究算法走向临床检测所需的质控、检出限、内参和不一致结果分析框架。

### P5. Pulmonary Metagenomic Sequencing Suggests Missed Infections in Immunocompromised Children

- **作者 / 期刊**：Zinter MS et al.; *Clinical Infectious Diseases*
- **发表日期**：2019-05-01
- **DOI**：[10.1093/cid/ciy802](https://doi.org/10.1093/cid/ciy802)
- **PMID**：[30239621](https://pubmed.ncbi.nlm.nih.gov/30239621/)
- **简单摘要**：对 34 名免疫受损儿童的 41 份下呼吸道样本平行提取 RNA/DNA 并测序，发现细菌、真菌、RNA 和 DNA 病毒构成的复杂微生物群。研究以样本内绝对丰度、相对其他样本的离群程度及多样性变化识别潜在病原。
- **课题价值**：说明“检出微生物”不等于“致病”，病原模型必须加入背景队列、生态多样性和宿主状态。

### P6. Nanopore metagenomics enables rapid clinical diagnosis of bacterial lower respiratory infection

- **作者 / 期刊**：Charalampous T et al.; *Nature Biotechnology*
- **发表日期**：2019-06-24
- **DOI**：[10.1038/s41587-019-0156-5](https://doi.org/10.1038/s41587-019-0156-5)
- **PMID**：[31235920](https://pubmed.ncbi.nlm.nih.gov/31235920/)
- **简单摘要**：通过皂苷去除大量宿主 DNA，并用纳米孔测序实现约 6 小时的细菌性下呼吸道感染诊断和耐药基因识别。初始相对培养的敏感度高但特异度有限；加入 qPCR 和条件致病菌特异基因分析后，性能明显改善。
- **课题价值**：说明宿主核酸去除、耐药基因和二次确认规则是病原侧流水线的重要组成部分。

### P7. Clinical metagenomics

- **作者 / 期刊**：Chiu CY, Miller SA; *Nature Reviews Genetics*
- **发表日期**：2019-06-01
- **DOI**：[10.1038/s41576-019-0113-7](https://doi.org/10.1038/s41576-019-0113-7)
- **PMID**：[30918369](https://pubmed.ncbi.nlm.nih.gov/30918369/)
- **研究类型**：综述
- **简单摘要**：综述临床 mNGS 对患者样本中微生物与宿主 DNA/RNA 的综合分析，覆盖病原诊断、耐药性、微生物组、宿主表达和临床实验室落地挑战。
- **课题价值**：可作为论文中“为何需要联合宿主与病原证据”以及标准化、解释和监管问题的核心综述。

### P8. Clinical Metagenomic Sequencing for Diagnosis of Meningitis and Encephalitis

- **作者 / 期刊**：Wilson MR et al.; *The New England Journal of Medicine*
- **发表日期**：2019-06-01
- **DOI**：[10.1056/nejmoa1803396](https://doi.org/10.1056/nejmoa1803396)
- **PMID**：[31189036](https://pubmed.ncbi.nlm.nih.gov/31189036/)
- **简单摘要**：多中心前瞻性研究纳入 204 名疑似脑膜炎/脑炎患者，最终诊断 58 例中枢神经系统感染。mNGS 额外发现 13 例常规来源医院检测未识别的感染，其中 8 例可能影响临床处理；漏检多与低病原滴度或病原只存在于其他组织有关。
- **课题价值**：为诊断增益、临床行动性、正交确认和假阴性原因分类提供高质量临床证据。

### P9. IDseq-An open source cloud-based pipeline and analysis service for metagenomic pathogen detection and monitoring

- **作者 / 期刊**：Kalantar KL et al.; *GigaScience*
- **发表日期**：2020-10-01
- **DOI**：[10.1093/gigascience/giaa111](https://doi.org/10.1093/gigascience/giaa111)
- **PMID**：[33057676](https://pubmed.ncbi.nlm.nih.gov/33057676/)
- **简单摘要**：提出开源云端病原分析平台 IDseq（现 CZ ID），从原始读段执行宿主/质量过滤、组装与分类比对，并提供背景模型、内参识别和可视化。研究还用模拟进化病毒与真实新发病毒样本评估新病原发现能力。
- **课题价值**：可参考其可复现流水线、背景分布、样本质控和面向非生信用户的报告界面设计。

### P10. Rapid pathogen detection by metagenomic next-generation sequencing of infected body fluids

- **作者 / 期刊**：Gu W et al.; *Nature Medicine*
- **发表日期**：2020-11-09
- **DOI**：[10.1038/s41591-020-1105-z](https://doi.org/10.1038/s41591-020-1105-z)
- **PMID**：[33169017](https://pubmed.ncbi.nlm.nih.gov/33169017/)
- **简单摘要**：利用体液游离 DNA 建立 mNGS 检测，在 160 名急症患者的 182 份体液中评估 Illumina 和纳米孔平台。对培养/PCR 阴性但最终证实感染的 12 例中检出 7 例，纳米孔实时分析的样本到结果中位时间约 6 小时。
- **课题价值**：适合用于比较不同测序平台、样本类型和周转时间；同时提醒游离 DNA 反映的是病原存在而非转录活性。

### P11. Metatranscriptomics: A Tool for Clinical Metagenomics

- **作者 / 期刊**：Tyagi S, Katara P; *OMICS: A Journal of Integrative Biology*
- **发表日期**：2024-07-19
- **DOI**：[10.1089/omi.2024.0130](https://doi.org/10.1089/omi.2024.0130)
- **PMID**：[39029911](https://pubmed.ncbi.nlm.nih.gov/39029911/)
- **研究类型**：综述
- **简单摘要**：比较 16S、宏基因组与宏转录组，强调宏转录组能够描述微生物群中正在活跃表达的基因。文章梳理 RNA 提取、测序、特征定量、差异表达、统计分析工具及其优缺点。
- **课题价值**：可用于界定“病原存在”和“病原活跃”两个不同目标，并支持病原转录活性特征设计。

### P12. DEMINERS enables clinical metagenomics and comparative transcriptomic analysis by increasing throughput and accuracy of nanopore direct RNA sequencing

- **作者 / 期刊**：Song J et al.; *Genome Biology*
- **发表日期**：2025-03-28
- **DOI**：[10.1186/s13059-025-03536-3](https://doi.org/10.1186/s13059-025-03536-3)
- **PMID**：[40155949](https://pubmed.ncbi.nlm.nih.gov/40155949/)
- **简单摘要**：提出纳米孔直接 RNA 测序工具 DEMINERS，将 RNA 多重化、随机森林条形码分类和物种特异卷积神经网络碱基识别结合，可复用最多 24 个样本。其应用覆盖临床宏基因组、病原 RNA 及 RNA 修饰分析。
- **课题价值**：如果课题计划处理直接 RNA 纳米孔数据，该研究可作为病原转录本和修饰层联合分析的前沿方法参考。

### P13. Metatranscriptomic profiling reveals pathogen and host response signatures of pediatric acute sinusitis and upper respiratory infection

- **作者 / 期刊**：Doxey AC et al.; *Genome Medicine*
- **发表日期**：2025-03-17
- **DOI**：[10.1186/s13073-025-01447-3](https://doi.org/10.1186/s13073-025-01447-3)
- **PMID**：[40098147](https://pubmed.ncbi.nlm.nih.gov/40098147/)
- **简单摘要**：对 221 名儿童鼻咽样本进行无靶向 RNA-seq。相对培养，三种鼻窦炎相关细菌的检测敏感度/特异度为 87%/81%；相对 qRT-PCR，12 种呼吸道病毒为 86%/92%；同时检出额外病原、重建病毒基因组并发现细菌/病毒特异宿主反应。
- **课题价值**：与本课题高度一致，证明单次宏转录组数据可以同时支持病原识别、宿主免疫判断和监测分析。

## 6. 双 RNA-seq 与单细胞宿主-病原互作

### D1. Dual RNA-seq of pathogen and host

- **作者 / 期刊**：Westermann AJ et al.; *Nature Reviews Microbiology*
- **发表日期**：2012-09-01
- **DOI**：[10.1038/nrmicro2852](https://doi.org/10.1038/nrmicro2852)
- **PMID**：[22890146](https://pubmed.ncbi.nlm.nih.gov/22890146/)
- **研究类型**：综述
- **简单摘要**：提出并评估在不预先物理分离病原和宿主细胞的情况下，使用 RNA-seq 同时分析双方表达变化的 dual RNA-seq 思路，奠定该领域的方法学框架。
- **课题价值**：适合用于定义课题中的“双转录组”和说明其相对单边宿主转录组的增量信息。

### D2. Comprehensive insights into transcriptional adaptation of intracellular mycobacteria by microbe-enriched dual RNA sequencing

- **作者 / 期刊**：Rienksma RA et al.; *BMC Genomics*
- **发表日期**：2015-02-05
- **DOI**：[10.1186/s12864-014-1197-2](https://doi.org/10.1186/s12864-014-1197-2)
- **PMID**：[25649146](https://pubmed.ncbi.nlm.nih.gov/25649146/)
- **简单摘要**：针对感染细胞中分枝杆菌 RNA 比宿主 RNA 低约 1000 倍的问题，结合微生物转录本富集和特异性 rRNA 去除完成双 RNA-seq。研究同时观察到细菌胆固醇降解/铁获取上调与宿主胆固醇合成补偿。
- **课题价值**：直接揭示病原/宿主读段极度不平衡的实验挑战，以及富集策略可能引入的定量偏差。

### D3. Pathogen Cell-to-Cell Variability Drives Heterogeneity in Host Immune Responses

- **作者 / 期刊**：Avraham R et al.; *Cell*
- **发表日期**：2015-09-03
- **DOI**：[10.1016/j.cell.2015.08.027](https://doi.org/10.1016/j.cell.2015.08.027)
- **PMID**：[26343579](https://pubmed.ncbi.nlm.nih.gov/26343579/)
- **简单摘要**：把单细胞 RNA-seq 与荧光感染表型结合，发现单个沙门菌的 PhoPQ 活性差异可通过 LPS 修饰驱动巨噬细胞不同程度的 I 型干扰素反应，建立了病原异质性与宿主免疫异质性的因果联系。
- **课题价值**：说明 bulk 数据会掩盖感染细胞比例和病原状态差异，可为去卷积、不确定性解释与单细胞扩展提供依据。

### D4. Dual RNA-seq unveils noncoding RNA functions in host-pathogen interactions

- **作者 / 期刊**：Westermann AJ et al.; *Nature*
- **发表日期**：2016-01-20
- **DOI**：[10.1038/nature16547](https://doi.org/10.1038/nature16547)
- **PMID**：[26789254](https://pubmed.ncbi.nlm.nih.gov/26789254/)
- **简单摘要**：在沙门菌感染中同时分析病原与宿主 RNA，发现细菌小 RNA PinT 对侵袭效应因子和胞内生存毒力基因进行时间调控，并通过跨物种相关分析将其与宿主 JAK-STAT 通路和感染特异长链非编码 RNA 联系起来。
- **课题价值**：为构建“病原基因模块-宿主免疫通路”的跨物种关联网络和机制解释层提供经典范例。

### D5. Time-resolved dual RNA-seq reveals extensive rewiring of lung epithelial and pneumococcal transcriptomes during early infection

- **作者 / 期刊**：Aprianto R et al.; *Genome Biology*
- **发表日期**：2016-09-27
- **DOI**：[10.1186/s13059-016-1054-5](https://doi.org/10.1186/s13059-016-1054-5)
- **PMID**：[27678244](https://pubmed.ncbi.nlm.nih.gov/27678244/)
- **简单摘要**：在人肺泡上皮细胞-肺炎链球菌感染体系中开展时间分辨 dual RNA-seq。研究同时揭示宿主氧化应激、病原感受态调控、黏附菌对先天免疫的抑制，以及宿主黏蛋白驱动病原糖转运等互作过程。
- **课题价值**：提示时间是重要预测变量；可借鉴动态通路评分、滞后关联和病原-宿主互作网络设计。

### D6. Single-cell RNA-seq ties macrophage polarization to growth rate of intracellular Salmonella

- **作者 / 期刊**：Saliba AE et al.; *Nature Microbiology*
- **发表日期**：2016-11-14
- **DOI**：[10.1038/nmicrobiol.2016.206](https://doi.org/10.1038/nmicrobiol.2016.206)
- **PMID**：[27841856](https://pubmed.ncbi.nlm.nih.gov/27841856/)
- **简单摘要**：结合细菌分裂荧光报告和单细胞 RNA-seq，发现携带不生长沙门菌的巨噬细胞偏 M1 样，而携带快速生长细菌的细胞偏抗炎 M2 样，并存在连续的中间宿主状态。
- **课题价值**：说明病原活性与宿主免疫表型应联合解释，简单的病原丰度并不足以代表感染状态。

## 7. 智能体、LLM 与转录组基础模型

### A1. Transfer learning enables predictions in network biology

- **作者 / 期刊**：Theodoris CV et al.; *Nature*
- **发表日期**：2023-05-31
- **DOI**：[10.1038/s41586-023-06139-9](https://doi.org/10.1038/s41586-023-06139-9)
- **PMID**：[37258680](https://pubmed.ncbi.nlm.nih.gov/37258680/)
- **简单摘要**：提出 Geneformer，在约 3000 万个单细胞转录组上进行自监督预训练，再以少量任务数据微调用于基因网络、疾病状态和靶点预测。结果表明大规模预训练能为小样本网络生物学任务提供有效迁移。
- **课题价值**：可为宿主免疫转录本表示学习和小样本微调提供技术路线，但其输出仍需与传统基线、外部队列和生物学机制共同验证。

### A2. GeneGPT: augmenting large language models with domain tools for improved access to biomedical information

- **作者 / 期刊**：Jin Q et al.; *Bioinformatics*
- **发表日期**：2024-02-01
- **DOI**：[10.1093/bioinformatics/btae075](https://doi.org/10.1093/bioinformatics/btae075)
- **PMID**：[38341654](https://pubmed.ncbi.nlm.nih.gov/38341654/)
- **简单摘要**：通过上下文示例教 LLM 调用 NCBI Web API 回答基因组学问题，并用可执行 API 返回结果降低幻觉。GeneGPT 在 GeneTuring 八项任务上的平均得分为 0.83，高于多种检索增强或生物医学语言模型。
- **课题价值**：适合借鉴为“证据型智能体”：所有基因、通路、病原和文献解释均通过受控工具查询并保留来源，而非由 LLM 凭记忆生成。

### A3. scGPT: toward building a foundation model for single-cell multi-omics using generative AI

- **作者 / 期刊**：Cui H et al.; *Nature Methods*
- **发表日期**：2024-02-26
- **DOI**：[10.1038/s41592-024-02201-0](https://doi.org/10.1038/s41592-024-02201-0)
- **PMID**：[38409223](https://pubmed.ncbi.nlm.nih.gov/38409223/)
- **简单摘要**：在超过 3300 万个细胞上训练生成式 Transformer 基础模型 scGPT，并迁移到细胞类型注释、批次整合、多组学整合、扰动反应预测和基因网络推断等任务。
- **课题价值**：为单细胞宿主免疫表示和多组学融合提供基础模型参考，但并不直接等同于临床感染分类器或解释智能体。

### A4. CellAgent: LLM-Driven Multi-Agent Framework for Natural Language-Based Single-Cell Analysis

- **作者 / 来源**：Xiao Y et al.; *bioRxiv*
- **发表日期**：2024-05-15
- **DOI**：[10.1101/2024.05.13.593861](https://doi.org/10.1101/2024.05.13.593861)
- **研究类型**：**预印本，尚不能按同行评议结论使用**
- **简单摘要**：提出面向 scRNA-seq 与空间转录组的分层多智能体框架，通过自然语言规划端到端分析；配套 sc-Omni 工具集和自反思优化机制。作者报告其效率较人工专家流程提高约 60%，准确性与既有方法相当。
- **课题价值**：可作为“规划智能体-执行智能体-评估智能体-报告智能体”架构参考；任何性能结论都应因预印本身份而谨慎引用。

### A5. Integrating a host biomarker with a large language model for diagnosis of lower respiratory tract infection

- **作者 / 期刊**：Phan HV et al.; *Nature Communications*
- **发表日期**：2025-12-16
- **DOI**：[10.1038/s41467-025-66218-5](https://doi.org/10.1038/s41467-025-66218-5)
- **PMID**：[41402257](https://pubmed.ncbi.nlm.nih.gov/41402257/)
- **简单摘要**：将肺部宿主转录标志物 FABP4 与 GPT-4 对电子病历文本的评估相结合。联合模型在危重成人队列中 AUC 0.93、准确率 84%，优于单独标志物或单独 LLM；独立验证队列 AUC 0.98、准确率 96%。
- **课题价值**：这是“转录组模型 + LLM 临床语境分析”的直接先例；课题可进一步加入病原证据，并要求智能体展示证据来源和冲突处理。

### A6. Artificial Intelligence agents for biological research: a survey

- **作者 / 期刊**：Qi C et al.; *Briefings in Bioinformatics*
- **发表日期**：2026-01-01
- **DOI**：[10.1093/bib/bbag075](https://doi.org/10.1093/bib/bbag075)
- **PMID**：[41744224](https://pubmed.ncbi.nlm.nih.gov/41744224/)
- **研究类型**：综述
- **简单摘要**：系统回顾 100 余项生物研究智能体工作，提出覆盖任务领域、系统架构、交互方式、评估策略和资源集成的 5D 分类框架，并总结可靠性、隐私、扩展性与标准化评估等开放问题。
- **课题价值**：适合用于定义“智能体”而非普通聊天界面，并据此设计工具调用、反馈、自检、审计和基准评估。

## 8. 对毕业论文技术路线的直接启示

### 8.1 推荐的问题定义

不建议只做一个“细菌 vs 病毒”的平面分类器。更合理的层级输出是：

1. **感染性炎症 vs 非感染性炎症**：参考 Sepsis MetaScore、SeptiCyte Lab。
2. **病原类别**：细菌、病毒、真菌、混合感染、未确定。
3. **病原证据强度**：病原读段/转录活性、相对背景离群度、覆盖度、阴性对照污染概率。
4. **宿主免疫状态**：干扰素反应、髓系炎症、抗原呈递、免疫抑制/耗竭等模块。
5. **严重度/器官功能障碍风险**：与感染类型并行的多任务头，而非事后附加解释。
6. **不确定/拒判**：病原与宿主证据冲突、低质量样本或分布外样本应允许输出“不确定”。

### 8.2 推荐的模型结构

```text
病原 RNA 分支 ──> 物种/属丰度、覆盖度、活跃基因、毒力/耐药模块 ─┐
                                                               ├─> 中后期融合 ─> 感染类别/严重度/置信度
宿主 RNA 分支 ──> 免疫通路、细胞组成、基因签名、表达嵌入 ─────┘
临床协变量 ─────> 年龄、采样部位、用药、病程时间、实验批次 ────┘
```

优先从可解释基线开始：病原规则分数 + 宿主 logistic regression/LightGBM，再与神经网络或预训练嵌入比较。融合层应做病原单模态、宿主单模态、简单拼接和门控/注意力融合的消融实验，以证明联合信息确有增益。

### 8.3 数据划分与评价重点

- **按队列/医院/平台分组划分**，不能随机把同一队列的样本拆入训练和测试；特征选择、批次校正和阈值学习均须在训练折内部完成。
- 至少设置一次真正的**外部队列验证**，并报告年龄、感染部位、免疫抑制状态、病原类别和采样时间亚组。
- 除 AUROC 外，报告 AUPRC、敏感度、特异度、PPV、NPV、校准曲线/Brier score、决策曲线和拒判覆盖率。
- 对病原侧进行阴性对照、环境背景、试剂污染、宿主去除效率和检出限分析；对宿主侧控制细胞组成、激素/免疫抑制剂、抗菌药使用和疾病严重度混杂。
- 单独评估混合感染、定植/感染区分、低病原负荷和常规检测阴性病例，不把“微生物检出”直接当作感染金标准。

### 8.4 推荐的解释智能体边界

智能体适合做**受约束的分析编排和证据解释**，不应直接替代诊断模型：

1. 读取结构化模型输出、样本质控和关键特征，而不是直接从原始矩阵自由判断。
2. 调用固定版本的基因注释、通路、病原、耐药和文献数据库，并记录每次工具调用与版本。
3. 分别生成病原证据、宿主证据、二者一致性、冲突项、质量风险和结论置信度。
4. 每项机制解释绑定可验证的基因/通路/文献来源；找不到证据时明确标为假设。
5. 通过模板或 JSON Schema 约束输出，增加引用核查智能体和数值一致性检查。
6. 评估事实准确率、引用可追溯率、重复运行一致性、专家评分及错误严重度，而不只评估语言流畅度。

## 9. 可直接用于开题报告的研究空白概括

现有研究已分别证明宿主转录签名和无偏病原测序对感染诊断有价值，但仍存在四个可形成毕业论文创新点的空白：

1. **联合建模不足**：多数工作只分析病原或宿主单侧；真正统一处理病原活跃表达、宿主免疫状态与临床背景的研究仍较少。
2. **跨队列泛化不足**：宿主签名在不同年龄、平台、感染部位和免疫状态中性能波动明显，批次泄漏和单中心验证会高估效果。
3. **定植与感染难区分**：病原核酸检出不能单独证明致病，需结合病原转录活性、相对背景和宿主免疫响应。
4. **解释缺少可追溯性**：LLM 能整合文本与生物标志物，但幻觉、证据冲突、隐私和评价标准仍未解决；工具增强、结构化输出和审计轨迹是更稳妥的方向。

## 10. 元数据来源

- Europe PMC REST API：<https://www.ebi.ac.uk/europepmc/webservices/rest/search>
- PubMed：<https://pubmed.ncbi.nlm.nih.gov/>
- Crossref REST API：<https://api.crossref.org/works>
- DOI 解析：<https://doi.org/>

本文中文摘要依据数据库收录摘要压缩改写，未将其作为原文逐字翻译。正式引用时应以出版社页面和论文全文为准。
