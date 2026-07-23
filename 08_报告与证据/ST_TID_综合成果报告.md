# ^60Co γ 射线总剂量辐照下 S/T 组器件电学特性实验与 T 器件 Sentaurus 仿真研究

**综合成果报告**

**研究对象：** S/T 组器件 0-60 krad(Si) 累积辐照；T 组二维沟槽器件 Sentaurus TID 验证  
**报告性质：** 本人完成工作的研究型、可追溯成果汇总  
**版本日期：** 2026-07-23  
**编制：** 项目研究者（本人）

# 摘要

我围绕 ^60Co γ 射线总剂量效应完成了从实验设计、现场辐照、器件测试、原始数据统一重算、S/T 组间比较，到 T 器件 Sentaurus 建模、标定、误差诊断和证据归档的完整工作链。实验覆盖 S1-S3、T1-T3 六只纵向跟踪器件和 0、10、20、30、40、50、60 krad(Si) 七个剂量点；每 10 krad(Si) 的照射时间为 198 s，辐照偏置为 20 V，室温测试。原始工作簿中的 GM/VT 共含 42 个 `#REF`，我没有沿用错误结果，而是从 DrainI-GateV 原始列按统一算法重算 42 条转移记录，并整理 55 条输出记录与 13 条 S 组复扫记录。

实验结果直接显示：60 krad(Si) 时，S 组与 T 组阈值漂移分别为 −6.120±0.045 V 和 −9.969±0.337 V，峰值跨导分别下降 60.25±1.96% 和 61.21±4.10%；T 组亚阈值摆幅由 225.4±2.8 mV/dec 增至 1674.0±35.4 mV/dec，增量约为 S 组的 10.8 倍。输出响应与转移退化并不平行：S 组 30 V 漏电增加 1840±992%，V@1 µA 从 106.3±6.4 V 降至 35.3±0.6 V；T 组 30 V 漏电仅增加 60.2±11.9%，V@1 µA 反而从 92.7±1.2 V 升至 108.0±1.0 V。S 组 13 条后续扫描的 30 V 漏电均低于同器件同剂量首扫，降幅为 70.65%-96.19%，该结果只支持“扫描历史相关响应”，不证明唯一恢复机制。

T 器件仿真采用不可变 `Trench VDMOS.gzp` 和真实 VM Sentaurus/SVisual 证据。七剂量共同参与标定后，ΔVth RMSE 为 0.0771 V，60 krad ΔVth 误差为 0.00177 V，gm 变化 RMSE 为 5.97 个百分点；因此这些误差描述标定质量，不是盲测预测精度。60 krad SS 仿真/实测为 892/1674 mV/dec，暴露了均匀陷阱模型的表达边界。D30 仅有 15.6-30 V、17 点，状态为 QUALIFIED_PARTIAL；D40 有 0.003-30 V、163 点且保留 6 个低压负点。仿真 V@1 µA 为 BLOCKED，IIC 或 Id@30 V 均不能替代。S 组仿真与应力恢复仿真不适用于本次 T-only campaign。

**关键词：** ^60Co γ 射线；总电离剂量；阈值电压；跨导；亚阈值摆幅；漏电；Sentaurus；证据链

## 摘要指标表

| 成果块 | 本人完成的工作与定量结果 | 证据边界 |
|---|---|---|
| 完整工作链 | 28 个原始工作簿；42 条转移、55 条输出、13 条复扫；统一图表和附录 | 原始文件只读，派生结果可回溯 |
| S 组退化 | 60 krad ΔVth=−6.120±0.045 V；gm=−60.25±1.96%；SS=321.9±30.7 mV/dec | n=3，本批器件描述 |
| T 组退化 | 60 krad ΔVth=−9.969±0.337 V；gm=−61.21±4.10%；SS=1674.0±35.4 mV/dec | 不由差异反推未公开结构 |
| S 组复扫 | 13/13 条 30 V 漏电降低 70.65%-96.19% | 扫描历史相关，不等于机制证明 |
| T 转移仿真 | ΔVth RMSE 0.0771 V；gm RMSE 5.97 pct-pt | 七剂量共同标定，不是盲测 |
| 输出/高场边界 | D30 partial；D40 带 6 个负点；V@1µA BLOCKED | 不得称 BV 拟合，不得替代指标 |

# 工作内容与技术路线

我把研究拆成实验闭环和仿真闭环。实验闭环以同一器件纵向跟踪为主线，在统一偏置与剂量节点下完成辐照和电学测试，再从原始列重算参数；仿真闭环以 T 实验提出问题，固定结构和运行边界，只用低参数剂量映射标定主趋势，并把失败、缺段、异常与不可比较指标作为正式结论的一部分。

![图0-1 本项目研究闭环（项目原创流程资产；SUPPORTED：用于说明工作组织，不替代数据证据）](assets/route.png)

*图0-1 本项目研究闭环（项目原创流程资产；SUPPORTED：用于说明工作组织，不替代数据证据）*

> 证据分层约定：**SUPPORTED** 表示由正式实验派生数据或完整仿真证据链直接支持；**QUALIFIED** 表示可用但带覆盖、异常或统计限制；**BLOCKED** 表示当前证据不允许定量比较或正向断言。

# 第一部分 S/T 组器件辐照实验与对比

# 第1章 实验任务、现场与统一分析方法

## 1.1 实验设计与样品口径

S1-S3、T1-T3 是跨剂量持续跟踪的六只物理器件，不是每个剂量重新抽样。剂量点为 0-60 krad(Si)，步进 10 krad(Si)，每步照射 198 s；辐照期间施加 20 V 偏置并采用限流保护，实验在室温环境下完成。S/T 仅是样品组标签；结构、材料、尺寸、工艺与封装信息不在现有公开记录内，我不根据电学差异反推内部结构。

转移测试固定 VDS=0.1 V。输出测试固定 VGS=−20 V，VDS 从 0 扫至 150 V；大量曲线高压端进入约 10 mA 合规区，因此 150 V 电流不作为正式剂量指标。主分析使用 10、20、30 V 的共同安全点、V@1 µA 以及合规起始电压。

## 1.2 本次项目现场过程证据

![图1-1 本次项目辐照台现场照片（SUPPORTED：过程证据；不补写无记录的设备参数）](assets/site_irradiator.jpg)

*图1-1 本次项目辐照台现场照片（SUPPORTED：过程证据；不补写无记录的设备参数）*

![图1-2 本次项目辐照室外部现场照片（SUPPORTED：过程证据）](assets/site_room.jpg)

*图1-2 本次项目辐照室外部现场照片（SUPPORTED：过程证据）*

![图1-3 本次项目钴源相关现场照片（SUPPORTED：过程证据；不用于推导剂量率）](assets/site_source.jpg)

*图1-3 本次项目钴源相关现场照片（SUPPORTED：过程证据；不用于推导剂量率）*

三张照片仅证明本次项目的现场过程。现有记录没有给出可核验的剂量率与剂量学不确定度，所以我保留“每 10 krad(Si) 对应 198 s”这一直接记录，不自行换算标准剂量率。

## 1.3 统一重算与统计方法

原始 Excel 的 GM/VT 列共出现 42 个 `#REF`。我从 DrainI-GateV 原始列重新计算：漏极电流先用 11 点二阶 Savitzky-Golay 滤波，在 VGS 轴上求导得到 gm，以 gm 峰值处切线与电压轴的交点定义 Vth；SS 采用 21 点滑动窗口拟合 log10|ID|-VGS，只保留 R²≥0.98 的最佳窗口。所有剂量变化均按同一器件相对 0 krad(Si) 基线计算。

每个组别在每个剂量点均为 n=3，报告均值±样本标准差，不进行总体显著性外推。输出主汇总仅纳入 scan_no=1；S 组 scan_no>1 只与同一器件、同一剂量首扫配对，不能增加独立样本量。半对数图对带符号电流取绝对值仅用于数量级显示，不把低电流负点解释为物理反向导电。

| 方法项 | 正式口径 | 主要边界 |
|---|---|---|
| Vth | 11点二阶SG滤波；gm峰值切线外推 | 受扫描范围和局部曲线形状影响 |
| gm | 平滑 ID 对 VGS 数值梯度的峰值 | 用于同算法相对比较 |
| SS | 21点滑窗；R²≥0.98 | 窗口可位于不同电压区段 |
| 30 V漏电 | VGS=−20 V；共同安全偏压插值 | 不代表完整高压耐受 |
| V@1µA | 首次达到 1 µA 的离散 VDS | 受 1 V 步进、突变和合规影响 |
| 复扫 | 同器件同剂量配对 | 不平衡重复，不作独立样本 |

# 第2章 S 组实验结果

## 2.1 转移特性与阈值漂移

![图2-1 S组七剂量转移特性（线性坐标；SUPPORTED）](assets/transfer_linear_S.png)

*图2-1 S组七剂量转移特性（线性坐标；SUPPORTED）*

![图2-2 S组七剂量转移特性（半对数坐标；SUPPORTED）](assets/transfer_semilog_S.png)

*图2-2 S组七剂量转移特性（半对数坐标；SUPPORTED）*

数据直接显示，S 组转移曲线随剂量持续向负 VGS 方向移动。Vth 从 2.073±0.014 V 变为 −4.047±0.035 V，60 krad 配对 ΔVth 为 −6.120±0.045 V。三只器件的变化方向一致，说明趋势不是由单个离群器件独立造成；但 n=3 仍只描述本批样品。

## 2.2 S组七剂量完整组均值表

| 剂量/krad(Si) | Vth/V | ΔVth/V | gm变化/% | SS/(mV/dec) | \|Id\|@30V/A | V@1µA/V |
|---|---|---|---|---|---|---|
| 0 | 2.073 ± 0.014 | 0.000 ± 0.000 | 0.00 ± 0.00 | 188.3 ± 1.0 | 8.66e-10 ± 3.37e-10 | 106.3 ± 6.4 |
| 10 | 0.967 ± 0.010 | -1.106 ± 0.011 | -33.23 ± 1.16 | 215.8 ± 25.6 | 4.85e-09 ± 6.53e-09 | 51.0 ± 10.4 |
| 20 | -0.079 ± 0.011 | -2.152 ± 0.017 | -44.09 ± 1.20 | 227.3 ± 26.2 | 1.72e-08 ± 2.80e-08 | 46.0 ± 10.1 |
| 30 | -1.104 ± 0.019 | -3.177 ± 0.025 | -50.47 ± 1.07 | 257.5 ± 53.9 | 1.31e-08 ± 5.94e-09 | 35.3 ± 0.6 |
| 40 | -2.106 ± 0.024 | -4.179 ± 0.031 | -54.48 ± 1.23 | 238.4 ± 7.5 | 2.49e-08 ± 5.30e-09 | 34.0 ± 1.0 |
| 50 | -3.083 ± 0.032 | -5.156 ± 0.040 | -57.68 ± 1.08 | 280.4 ± 25.7 | 2.04e-08 ± 1.89e-08 | 36.0 ± 4.6 |
| 60 | -4.047 ± 0.035 | -6.120 ± 0.045 | -60.25 ± 1.96 | 321.9 ± 30.7 | 1.52e-08 ± 5.53e-09 | 35.3 ± 0.6 |

表2-1 S组七剂量组均值±样本标准差（SUPPORTED；n=3）。

## 2.3 gm 与 SS

S 组 gm 从 0.1481±0.0050 S 降至 0.05883±0.00133 S，60 krad 相对下降 60.25±1.96%。SS 从 188.3±1.0 mV/dec 增至 321.9±30.7 mV/dec。MOS TID 文献把负向阈值移动与氧化层陷阱正电荷联系起来，并指出界面态与近界面缺陷会影响亚阈值区和迁移率相关性能[1-4]；本实验未直接测量陷阱谱，所以这些只构成物理框架，不构成缺陷分量的直接分离。

## 2.4 输出、低压漏电与高电流门槛

![图2-3 S组输出特性，VGS=−20 V（SUPPORTED；高压合规段不作本征解释）](assets/output_semilog_S.png)

*图2-3 S组输出特性，VGS=−20 V（SUPPORTED；高压合规段不作本征解释）*

60 krad 时，S 组 30 V 漏电由 (8.66±3.37)×10⁻¹⁰ A 增至 (1.52±0.55)×10⁻⁸ A，相对基线平均增加 1840±992%。但 10-60 krad 的均值并非严格单调，器件间离散显著。V@1 µA 从 106.3±6.4 V 降至 35.3±0.6 V。固定低压漏电与曲线达到更高电流所需电压描述不同区段，二者不能相互替代。

## 2.5 连续复扫：完整13条配对结果

![图2-4 S组13条复扫在30 V处相对首扫的漏电降低（QUALIFIED：配对扫描历史证据）](assets/stress_recovery_30v.png)

*图2-4 S组13条复扫在30 V处相对首扫的漏电降低（QUALIFIED：配对扫描历史证据）*

| 器件 | 剂量 | 复扫序号 | 首扫\|Id\|@30V/A | 复扫\|Id\|@30V/A | 降低/% |
|---|---|---|---|---|---|
| S1 | 30 | 2 | 7.726e-09 | 1.452e-09 | 81.21 |
| S1 | 60 | 2 | 1.153e-08 | 2.536e-09 | 78.01 |
| S2 | 30 | 2 | 1.222e-08 | 1.565e-09 | 87.20 |
| S2 | 40 | 2 | 2.442e-08 | 1.453e-09 | 94.05 |
| S2 | 50 | 2 | 1.574e-08 | 2.155e-09 | 86.31 |
| S2 | 60 | 2 | 2.154e-08 | 4.493e-09 | 79.14 |
| S3 | 20 | 2 | 4.960e-08 | 2.032e-09 | 95.90 |
| S3 | 40 | 2 | 3.039e-08 | 2.061e-09 | 93.22 |
| S3 | 50 | 2 | 4.120e-08 | 1.941e-09 | 95.29 |
| S3 | 50 | 3 | 4.120e-08 | 1.570e-09 | 96.19 |
| S3 | 60 | 2 | 1.247e-08 | 3.124e-09 | 74.95 |
| S3 | 60 | 3 | 1.247e-08 | 3.017e-09 | 75.80 |
| S3 | 60 | 4 | 1.247e-08 | 3.660e-09 | 70.65 |

表2-2 S组13条后续扫描完整配对表（QUALIFIED；13条均下降70.65%-96.19%，但不是13个独立器件）。

我把该结果表述为扫描历史相关响应。偏压/电场可能促进部分俘获电荷去俘获、中和或重新分布，相关候选路径与 Lelis 等关于偏压相关陷阱空穴退火以及 Oldham、Schwank 等综述的认识相容[1,2,8,9]。然而，自热、接触状态、前次高场改变后续初始条件、室温波动和低电流零点仍是替代解释。现有数据没有对照矩阵，不能把复扫结果写成已确定的恢复机制。

# 第3章 T 组实验结果

## 3.1 转移特性与完整组均值

![图3-1 T组七剂量转移特性（线性坐标；SUPPORTED）](assets/transfer_linear_T.png)

*图3-1 T组七剂量转移特性（线性坐标；SUPPORTED）*

![图3-2 T组七剂量转移特性（半对数坐标；SUPPORTED）](assets/transfer_semilog_T.png)

*图3-2 T组七剂量转移特性（半对数坐标；SUPPORTED）*

| 剂量/krad(Si) | Vth/V | ΔVth/V | gm变化/% | SS/(mV/dec) | \|Id\|@30V/A | V@1µA/V |
|---|---|---|---|---|---|---|
| 0 | 3.143 ± 0.032 | 0.000 ± 0.000 | 0.00 ± 0.00 | 225.4 ± 2.8 | 1.22e-10 ± 3.37e-12 | 92.7 ± 1.2 |
| 10 | 1.205 ± 0.068 | -1.937 ± 0.049 | -28.92 ± 8.05 | 603.2 ± 577.3 | 1.30e-10 ± 8.86e-12 | 98.3 ± 0.6 |
| 20 | -0.484 ± 0.126 | -3.627 ± 0.110 | -38.90 ± 6.21 | 1081.2 ± 623.8 | 1.54e-10 ± 4.08e-11 | 104.7 ± 0.6 |
| 30 | -2.121 ± 0.183 | -5.264 ± 0.170 | -47.10 ± 5.13 | 1541.6 ± 23.0 | 1.68e-10 ± 5.40e-11 | 107.3 ± 0.6 |
| 40 | -3.722 ± 0.244 | -6.865 ± 0.230 | -53.11 ± 4.51 | 1628.0 ± 64.6 | 1.61e-10 ± 1.59e-11 | 107.3 ± 0.6 |
| 50 | -5.284 ± 0.297 | -8.427 ± 0.284 | -57.91 ± 4.28 | 1639.2 ± 30.3 | 1.80e-10 ± 1.18e-11 | 107.3 ± 0.6 |
| 60 | -6.826 ± 0.350 | -9.969 ± 0.337 | -61.21 ± 4.10 | 1674.0 ± 35.4 | 1.95e-10 ± 1.20e-11 | 108.0 ± 1.0 |

表3-1 T组七剂量组均值±样本标准差（SUPPORTED；n=3）。

T 组 Vth 从 3.143±0.032 V 变为 −6.826±0.350 V，60 krad ΔVth 为 −9.969±0.337 V；gm 下降 61.21±4.10%。SS 从 225.4±2.8 mV/dec 增至 1674.0±35.4 mV/dec。10、20 krad 的 SS 标准差分别为 577.3 和 623.8 mV/dec，提示低中剂量阶段存在明显个体差异或窗口敏感性；到 30-60 krad，三只器件均进入约1515-1700 mV/dec区间。

## 3.2 输出响应

![图3-3 T组输出特性，VGS=−20 V（SUPPORTED）](assets/output_semilog_T.png)

*图3-3 T组输出特性，VGS=−20 V（SUPPORTED）*

T 组 30 V 漏电由 (1.219±0.034)×10⁻¹⁰ A 增至 (1.950±0.120)×10⁻¹⁰ A，60 krad 增加 60.2±11.9%；V@1 µA 由 92.7±1.2 V 升至 108.0±1.0 V。输出曲线的这一变化方向与阈值负移和 SS 恶化并不简单同步。由于 S/T 结构差异未公开，我只报告电学现象，不以组间差异推断器件设计。

# 第4章 S/T 组间对比与实验成果

## 4.1 转移参数同口径对比

![图4-1 S/T组阈值漂移对比（SUPPORTED）](assets/threshold_shift.png)

*图4-1 S/T组阈值漂移对比（SUPPORTED）*

![图4-2 S/T组峰值跨导相对变化（SUPPORTED）](assets/gm_change.png)

*图4-2 S/T组峰值跨导相对变化（SUPPORTED）*

![图4-3 S/T组亚阈值摆幅（SUPPORTED；T组中低剂量离散需保留）](assets/subthreshold_swing.png)

*图4-3 S/T组亚阈值摆幅（SUPPORTED；T组中低剂量离散需保留）*

在 60 krad，T 组 ΔVth 的绝对幅度比 S 组多约 3.85 V；两组 gm 均下降约 60%；T 组 SS 增量 1448.6 mV/dec，约为 S 组增量 133.6 mV/dec 的 10.8 倍。三项指标共同说明两组都发生显著转移退化，但退化维度不同，不能只用一个参数概括。

## 4.2 输出指标对比

![图4-4 S/T组30 V漏电对比（SUPPORTED；固定低压采样点）](assets/output_current_30v.png)

*图4-4 S/T组30 V漏电对比（SUPPORTED；固定低压采样点）*

![图4-5 S/T组实验V@1µA对比（SUPPORTED；离散步进代理）](assets/voltage_at_1ua.png)

*图4-5 S/T组实验V@1µA对比（SUPPORTED；离散步进代理）*

S 组 30 V 漏电增幅远大于 T 组，而 V@1 µA 在 S 组下降、在 T 组上升。这不是矛盾，而是说明固定低压电流和高电流门槛分别抽取曲线不同区段的信息。结合转移结果，我不作单一“耐辐照更好/更差”的排序。

## 4.3 我完成的实验成果

| 成果 | 完成量 | 可追溯证据 |
|---|---|---|
| 原始数据接收与保护 | 28个工作簿只读处理 | source_manifest.csv与SHA-256 |
| 统一重算 | 42条转移记录；清除42个#REF影响 | analysis_config.json、transfer_parameters.csv |
| 输出整理 | 55条输出记录；合规区剔除逻辑 | output_parameters.csv、data_quality_report.md |
| 扫描历史整理 | 13条复扫完整配对 | recovery_parameters.csv |
| 组间比较 | 七剂量S/T同口径表与13幅实验图 | transfer/output_summary.csv、03_figures |
| 成果边界 | n=3、结构保密、指标不可替代、机制不唯一 | 质控报告与本报告声明审计 |

# 第二部分 T 器件 Sentaurus 仿真与实验对比

# 第5章 仿真目标、模型与可追溯流程

## 5.1 从T实验提出问题

T 实验最稳定的共同趋势是阈值持续负移和 gm 下降；SS 的恶化更强，而输出指标与转移参数不平行。因此我把仿真目标限定为：在固定二维模型中复现 ΔVth/gm/SS 的主趋势，评估输出预击穿区和高场图能比较到何种程度，并把不能关闭的问题标为 QUALIFIED 或 BLOCKED。

## 5.2 固定模型与剂量映射

![图5-1 T器件二维结构与网格，来自真实VM SVisual（SUPPORTED）](assets/sim_structure_mesh.png)

*图5-1 T器件二维结构与网格，来自真实VM SVisual（SUPPORTED）*

上游 `Trench VDMOS.gzp` 在活动前后 SHA-256 均为 `4d09d17b88e9cb0fd0783875f9ec3446795d8b6bd3ba3b136d1bacb73da368bf`，状态为 VERIFIED_UNCHANGED_CAMPAIGN_COMPLETE。模型固定 P-body 掺杂 1.33×10¹⁷ cm⁻³、AreaFactor=30335、300 K、转移 VDS=0.1 V；输出使用 VGS=−20 V、无雪崩反馈。陷阱形状来自解包 deck 可追溯的均匀 Acceptor 设定。

剂量到陷阱密度采用低参数单调映射：Not(D)=3.0×10¹⁰+4.96×10¹²(D/60)^0.87 cm⁻²；Nit(D)=1.4×10¹¹+4.0×10¹²(D/60)^0.70 cm⁻²。七个剂量点共同参与参数标定，因此后续 RMSE 是标定范围内一致性，不是留出剂量上的盲测预测。

## 5.3 单核租约与正式证据链

每个 SDevice 进程均经 VM 侧原子单核租约执行 `sdevice --threads 1`，并保留 lease acquisition/release、CPU affinity、deck、PLT、solver log/stdout、终态偏压检查、解析 CSV 和哈希。网格→依赖电学求解→提取链保持串行。方法来源保留为 `E:\VDMOS_TID_Research` 的仓库指导、sentaurus-vm-runner、并行核心调度策略与 VM 笔记；本报告没有启动任何新 TCAD 计算，只重用正式交付证据。

| 链条环节 | 正式证据 | 判定 |
|---|---|---|
| 不可变输入 | GZP前后哈希一致 | SUPPORTED |
| 运行约束 | 原子单核lease与affinity验证 | SUPPORTED |
| 数值结果 | deck+PLT+log+终态偏压 | SUPPORTED/QUALIFIED |
| 曲线提取 | 真实VM SVisual；原始点保留 | SUPPORTED |
| 展示资产 | Origin叠加与SVisual分开标识 | SUPPORTED |
| 失败/重试 | 旧D30与高场失败证据保留 | HISTORICAL，不进入当前曲线 |

# 第6章 T仿真与T实验的转移特性对比

## 6.1 七剂量曲线与指标

![图6-1 T组实验—仿真转移特性半对数叠加（SUPPORTED；七剂量共同标定）](assets/sim_transfer_semilog.png)

*图6-1 T组实验—仿真转移特性半对数叠加（SUPPORTED；七剂量共同标定）*

![图6-2 T组实验—仿真转移指标对比（SUPPORTED/QUALIFIED）](assets/sim_transfer_metrics.png)

*图6-2 T组实验—仿真转移指标对比（SUPPORTED/QUALIFIED）*

| 剂量 | 实验ΔVth/V | 仿真ΔVth/V | 误差/V | 实验gm变化/% | 仿真gm变化/% | 实验SS | 仿真SS |
|---|---|---|---|---|---|---|---|
| 0 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 225 | 232 |
| 10 | -1.937 | -1.797 | 0.140 | -28.92 | -38.28 | 603 | 420 |
| 20 | -3.627 | -3.520 | 0.107 | -38.90 | -48.05 | 1081 | 538 |
| 30 | -5.264 | -5.184 | 0.080 | -47.10 | -53.74 | 1542 | 638 |
| 40 | -6.865 | -6.807 | 0.057 | -53.11 | -57.76 | 1628 | 729 |
| 50 | -8.427 | -8.400 | 0.027 | -57.91 | -60.80 | 1639 | 813 |
| 60 | -9.969 | -9.967 | 0.002 | -61.21 | -63.22 | 1674 | 892 |

表6-1 七剂量完整实验—仿真表。ΔVth RMSE=0.0771 V，60 krad误差=0.00177 V；gm变化RMSE=5.97个百分点，60 krad仿真/实测=−63.22%/−61.21%。

## 6.2 标定质量而非盲测预测

七个剂量点都参与了 Not/Nit 映射标定，所以这些小误差不能写成未知剂量预测能力。我将它们解释为：在当前 T 器件、300 K、0-60 krad(Si) 的标定范围内，低参数单调映射可以复现阈值负移和 gm 衰减的主要趋势。要评价预测能力，需要预先冻结参数并留出独立剂量、独立器件或不同偏置条件。

## 6.3 SS残差与模型辨识边界

60 krad SS 为 892/1674 mV/dec（仿真/实测）。参数扫描显示，继续增加同一均匀 Acceptor 陷阱虽然可提高 SS，却会过度压低 gm。因此我没有通过无约束增加陷阱来掩盖残差。该残差提示当前均匀陷阱近似不能同时辨识界面态谱、空间非均匀性、迁移率退化和实验窗口效应的全部贡献。

# 第7章 T输出与高场结果

## 7.1 预击穿输出与30 V电流

![图7-1 T组实验—仿真预击穿输出半对数对比（QUALIFIED；不得称BV拟合）](assets/sim_output_semilog.png)

*图7-1 T组实验—仿真预击穿输出半对数对比（QUALIFIED；不得称BV拟合）*

![图7-2 T组实验—仿真30 V电流（QUALIFIED；Id@30不能替代V@1µA）](assets/sim_id30.png)

*图7-2 T组实验—仿真30 V电流（QUALIFIED；Id@30不能替代V@1µA）*

D30 当前 run 从 checkpoint_14 独立续跑并 exit 0，真实 SVisual 仅得到 15.6-30 V 的17点，30 V电流为9.49939128786×10⁻⁹ A，状态为 QUALIFIED_PARTIAL。0.003-15.6 V 没有当前观测数据，不补点、不插值、不平滑、不拼接历史曲线。D40 当前 run 有163点，覆盖0.003-30 V，30 V电流为1.37863878805×10⁻⁸ A；6个低压负点原样保留，限定为可复现数值异常，不写成物理跃迁。

| 对象/指标 | 数据状态 | 允许的解释 | 禁止替代或外推 |
|---|---|---|---|
| D30输出 | QUALIFIED_PARTIAL；15.6-30 V；17点 | 当前高压子区间与30 V点 | 不得写成完整0.003-30 V |
| D40输出 | PROMOTABLE；0.003-30 V；163点 | 当前预击穿曲线 | 6个负点不得删除或物理化 |
| 实验V@1µA | SUPPORTED；0-150 V实验曲线代理 | 实验曲线形状指标 | 不能与Id@30混同 |
| 仿真V@1µA | BLOCKED | 无有效完整代理 | IIC和Id@30均不能替代 |
| IIC | 特定偏压/收敛条件下的高场指标 | 单独报告 | 不能称实验V@1µA |
| S组/应力恢复仿真 | NOT APPLICABLE | T-only campaign范围外 | 不得宣称完成 |

## 7.2 高场图与解释边界

![图7-3 T器件高压上下文（QUALIFIED；作为边界说明，不作击穿拟合验收结论）](assets/sim_high_voltage_context.png)

*图7-3 T器件高压上下文（QUALIFIED；作为边界说明，不作击穿拟合验收结论）*

![图7-4 0 krad预击穿终态电场，真实VM SVisual（SUPPORTED图像证据）](assets/sim_field_0.png)

*图7-4 0 krad预击穿终态电场，真实VM SVisual（SUPPORTED图像证据）*

![图7-5 60 krad预击穿终态电场，真实VM SVisual（SUPPORTED图像证据）](assets/sim_field_60.png)

*图7-5 60 krad预击穿终态电场，真实VM SVisual（SUPPORTED图像证据）*

两幅电场图允许比较当前求解终态下可见场分布及其相对变化，但截图本身不能证明击穿位置、雪崩主导路径或某一微观失效机制。特别是不同剂量终态偏压和收敛状态必须随图解释，不能只凭颜色强弱下结论。

# 第8章 综合讨论

## 8.1 S/T实验共同支持的TID框架

S/T 两组共同出现负向阈值漂移、gm 下降和 SS 恶化，与 MOS 氧化层中电荷产生、输运、俘获、界面态建立及随场/时间演化的通用 TID 框架一致[1-4]。阈值漂移主要反映等效电荷对栅控条件的改变；gm 与 SS 还受到迁移率、界面态和亚阈值输运的共同影响。这里的“支持”是现象层面相容，不等于直接测得 Not/Nit 或排除所有替代机制。

## 8.2 为什么转移和输出不平行

转移曲线在低 VDS 下强调栅控沟道，而输出测试在 VGS=−20 V、高 VDS 扫描下包含漂移区、边缘电场、接触、合规限制和测量历史。不同电场分布与电流路径使两类指标不必同向。S 组低压漏电大幅增加而 T 组 V@1µA 上升，正说明单一参数不足以给出“耐辐照优劣”。商业沟槽与分裂栅功率器件文献也报告了阈值、漏电和高场参数可能具有不同剂量响应[5-7,15]，但这些外部器件不能替代本项目实测。

## 8.3 T模型解释了什么，残差揭示了什么

低参数剂量映射解释了 T 组 ΔVth 和 gm 的主趋势，证明当前模型可作为标定范围内的定量描述工具。SS 残差、输出量级差异、D30缺段和D40负点则揭示：模型尚不足以统一解释界面态谱、空间非均匀陷阱、高场输运和实验测量历史。保留残差比无约束加参更能界定模型辨识能力。

## 8.4 扫描历史的候选解释与验证路径

S组复扫的方向一致性值得重视，但其设计并非平衡对照实验。偏压驱动的去俘获、隧穿中和或电荷重分布是可检验候选路径[8,9]；自热、接触、等待时间和合规历史仍需控制。下一轮应预注册静置时间、正反扫、扫速、偏置等待、温度与接触检查，并在S1-S3相同剂量点执行对照，以区分时间常数与电压历史。

# 第9章 成果、局限与下一步

## 9.1 我完成的成果

| 工作层级 | 本人完成的成果 | 定量或可追溯输出 |
|---|---|---|
| 实验 | 设计并完成七剂量纵向跟踪、测试和现场记录 | 6只器件、42条转移、55条输出 |
| 数据 | 修复分析链而不改原表 | 42个#REF绕开；统一SG/切线/SS算法 |
| 比较 | 建立S/T同口径证据体系 | 七剂量均值表、逐器件附录、13条复扫表 |
| TCAD | 建立T-only可追溯标定与问题关闭流程 | 7剂量转移；正式SVisual；单核lease |
| 诊断 | 保留残差、缺段和异常 | SS残差；D30 partial；D40负点 |
| 交付 | 形成MD/DOCX/PDF、资产、清单和QA | 可重复构建且源文件不变 |

## 9.2 本报告不支持的结论

| 不支持的结论 | 原因 |
|---|---|
| 理论正确已被证明 | 实验和标定只支持当前范围内的一致性 |
| 击穿拟合已获验收 | 当前主要是无雪崩预击穿输出与限定高场结果 |
| S组已形成正式全剂量仿真 | 本活动为T-only；S仿真不适用 |
| S组复扫已锁定唯一恢复机理 | 缺少平衡对照与直接陷阱测量 |
| 仿真V@1µA已获得 | 该指标为BLOCKED，IIC/Id@30不能替代 |
| D30获得完整曲线 | 当前仅15.6-30 V、17点 |

## 9.3 下一步任务

1. 产生独立、完整的 D30 低压 PLT 和全证据链，关闭 0.003-15.6 V 缺段；不得回填或拼接。
2. 冻结转移标定参数后，增加留出剂量或独立器件以评估预测能力。
3. 用受约束的界面态谱/空间非均匀方案分析 SS 残差，同时保持 gm 约束。
4. 为实验与仿真统一高压指标定义，分别报告 V@1µA、Id@30 和 IIC。
5. 对 S 复扫建立静置、扫速、正反扫、偏置与温度对照矩阵。

# 第10章 结论

1. 我完成了 S1-S3、T1-T3 六只器件在七个累计剂量点的纵向实验整理，并从原始 DrainI-GateV 列统一重算42条转移记录，避免42个`#REF`进入正式结论；统计范围仅代表每组n=3的本批样品。
2. 我确认60 krad时S/T组ΔVth分别为−6.120±0.045 V和−9.969±0.337 V，gm均下降约60%；T组SS增量约为S组的10.8倍，但该差异不能用于反推未公开结构。
3. 我证明输出响应不能由转移退化简单外推：S组30 V漏电增加1840±992%、V@1µA下降至35.3±0.6 V；T组30 V漏电仅增加60.2±11.9%、V@1µA升至108.0±1.0 V，因此不作单一耐辐照排序。
4. 我整理了S组13条复扫完整配对记录，30 V漏电均降低70.65%-96.19%；结论限定为扫描历史相关响应，去俘获、重分布、自热、接触和测量历史仍是并列候选解释。
5. 我完成了T器件七剂量Sentaurus标定，ΔVth RMSE=0.0771 V、gm变化RMSE=5.97个百分点；七剂量共同参与标定，所以这些数值是标定质量，不是盲测预测精度。
6. 我保留了模型和求解边界：60 krad SS仿真/实测为892/1674 mV/dec；D30仅15.6-30 V、17点且为QUALIFIED_PARTIAL；D40有163点并保留6个负点。
7. 我建立了不可变GZP、单核lease、真实SVisual、deck/PLT/log/CSV/hash证据链；仿真V@1µA为BLOCKED，IIC/Id@30不能替代，S组和应力恢复仿真不适用于T-only campaign。

# 参考文献

[1] Oldham T R, McLean F B. Total ionizing dose effects in MOS oxides and devices. IEEE Transactions on Nuclear Science, 2003, 50(3): 483-499. DOI: 10.1109/TNS.2003.812927.

[2] Schwank J R, Shaneyfelt M R, Fleetwood D M, et al. Radiation Effects in MOS Oxides. IEEE Transactions on Nuclear Science, 2008, 55(4): 1833-1853. DOI: 10.1109/TNS.2008.2001040.

[3] Fleetwood D M. Total Ionizing Dose Effects in MOS and Low-Dose-Rate-Sensitive Linear-Bipolar Devices. IEEE Transactions on Nuclear Science, 2013, 60(3): 1706-1730. DOI: 10.1109/TNS.2013.2259260.

[4] Ma T P, Dressendorfer P V, eds. Ionizing Radiation Effects in MOS Devices and Circuits. New York: Wiley, 1989. ISBN 978-0-471-84893-6.

[5] Wang R, Li Z, Qiao M, et al. Total Ionizing Dose Effects in 30-V Split-Gate Trench VDMOS. IEEE Transactions on Nuclear Science, 2020, 67(9): 2009-2014. DOI: 10.1109/TNS.2020.2965286.

[6] Liu S, DiCienzo C, Bliss M, et al. Analysis of Commercial Trench Power MOSFETs' Responses to Co-60 Irradiation. IEEE Transactions on Nuclear Science, 2008, 55(6): 3231-3236. DOI: 10.1109/TNS.2008.2008991.

[7] Li X, Cui J, Zheng Q, et al. Study of the Within-Batch TID Response Variability on Silicon-Based VDMOS Devices. Electronics, 2023, 12(6): 1403. DOI: 10.3390/electronics12061403.

[8] Lelis A J, Boesch H E, Oldham T R, McLean F B. Reversibility of trapped hole annealing. IEEE Transactions on Nuclear Science, 1988, 35(6): 1186-1191. DOI: 10.1109/23.25437.

[9] Lelis A J, Oldham T R, Boesch H E, McLean F B. The nature of the trapped hole annealing process. IEEE Transactions on Nuclear Science, 1989, 36(6): 1808-1815. DOI: 10.1109/23.45373.

[10] Gao B, Yu X, Ren D, et al. Total ionizing dose effects and annealing behavior for domestic VDMOS devices. Journal of Semiconductors, 2010, 31(4): 044007. DOI: 10.1088/1674-4926/31/4/044007.

[11] Sun Y, Wang T, Liu Z, Xu J. Investigation of irradiation effects and model parameter extraction for VDMOS field effect transistor exposed to gamma rays. Radiation Physics and Chemistry, 2021, 185: 109478. DOI: 10.1016/j.radphyschem.2021.109478.

[12] Sanchez Esqueda I, Barnaby H J, King M P. Compact Modeling of Total Ionizing Dose and Aging Effects in MOS Technologies. IEEE Transactions on Nuclear Science, 2015, 62(4): 1501-1515. DOI: 10.1109/TNS.2015.2414426.

[13] McWhorter P J, Winokur P S. Simple technique for separating the effects of interface traps and trapped-oxide charge in MOS transistors. Applied Physics Letters, 1986, 48(2): 133-135. DOI: 10.1063/1.96974.

[14] Sze S M, Ng K K. Physics of Semiconductor Devices, 3rd ed. Hoboken: Wiley, 2007. DOI: 10.1002/0470068329.

[15] Wang Y, Liu T, Dai Z, et al. Analysis of TID Effects on the Threshold Voltage and Breakdown Voltage of 100-V Split-Gate Trench VDMOS. IEEE Transactions on Electron Devices, 2024, 71(6): 3483-3489. DOI: 10.1109/TED.2024.3386661.

参考文献元数据以本地文献清单、Crossref/DOI核验记录和合法本地PDF为主逐项核对。文献截图只用于人工核验，不作为正文引文替代物。

# 附录A S1-S3、T1-T3逐器件转移参数全表

| 器件 | 剂量 | Vth/V | ΔVth/V | gm/S | gm变化/% | SS/(mV/dec) | SS R² |
|---|---|---|---|---|---|---|---|
| S1 | 0 | 2.057 | 0.000 | 0.14709 | 0.00 | 187.9 | 0.99994 |
| S1 | 10 | 0.958 | -1.099 | 0.09986 | -32.11 | 201.1 | 0.99932 |
| S1 | 20 | -0.084 | -2.141 | 0.08400 | -42.90 | 257.5 | 0.99978 |
| S1 | 30 | -1.107 | -3.164 | 0.07404 | -49.67 | 231.3 | 0.99841 |
| S1 | 40 | -2.106 | -4.163 | 0.06782 | -53.89 | 230.0 | 0.99927 |
| S1 | 50 | -3.078 | -5.135 | 0.06328 | -56.98 | 266.8 | 0.99936 |
| S1 | 60 | -4.031 | -6.088 | 0.06023 | -59.05 | 328.8 | 0.99921 |
| S2 | 0 | 2.085 | 0.000 | 0.14372 | 0.00 | 189.4 | 0.99993 |
| S2 | 10 | 0.966 | -1.119 | 0.09425 | -34.42 | 245.4 | 0.99987 |
| S2 | 20 | -0.087 | -2.171 | 0.08038 | -44.07 | 212.9 | 0.99976 |
| S2 | 30 | -1.121 | -3.206 | 0.07178 | -50.06 | 319.5 | 0.99976 |
| S2 | 40 | -2.130 | -4.215 | 0.06660 | -53.66 | 244.5 | 0.99959 |
| S2 | 50 | -3.118 | -5.202 | 0.06161 | -57.13 | 310.1 | 0.99922 |
| S2 | 60 | -4.087 | -6.172 | 0.05868 | -59.17 | 288.3 | 0.99903 |
| S3 | 0 | 2.077 | 0.000 | 0.15358 | 0.00 | 187.6 | 0.99993 |
| S3 | 10 | 0.977 | -1.100 | 0.10265 | -33.16 | 200.9 | 0.99959 |
| S3 | 20 | -0.066 | -2.143 | 0.08402 | -45.29 | 211.5 | 0.99978 |
| S3 | 30 | -1.085 | -3.161 | 0.07419 | -51.69 | 221.7 | 0.99918 |
| S3 | 40 | -2.082 | -4.159 | 0.06774 | -55.89 | 240.7 | 0.99959 |
| S3 | 50 | -3.054 | -5.131 | 0.06308 | -58.93 | 264.4 | 0.99937 |
| S3 | 60 | -4.022 | -6.099 | 0.05758 | -62.51 | 348.7 | 0.99954 |
| T1 | 0 | 3.140 | 0.000 | 0.13142 | 0.00 | 226.7 | 0.99992 |
| T1 | 10 | 1.148 | -1.991 | 0.10563 | -19.62 | 1269.8 | 0.99964 |
| T1 | 20 | -0.608 | -3.748 | 0.08972 | -31.73 | 361.0 | 0.99998 |
| T1 | 30 | -2.312 | -5.452 | 0.07730 | -41.19 | 1558.5 | 0.99997 |
| T1 | 40 | -3.976 | -7.116 | 0.06841 | -47.94 | 1608.0 | 0.99997 |
| T1 | 50 | -5.601 | -8.741 | 0.06173 | -53.03 | 1659.8 | 0.99998 |
| T1 | 60 | -7.199 | -10.339 | 0.05707 | -56.57 | 1698.3 | 0.99998 |
| T2 | 0 | 3.112 | 0.000 | 0.15980 | 0.00 | 222.2 | 0.99991 |
| T2 | 10 | 1.187 | -1.925 | 0.10627 | -33.50 | 272.6 | 0.99984 |
| T2 | 20 | -0.486 | -3.598 | 0.09135 | -42.83 | 1447.6 | 0.99991 |
| T2 | 30 | -2.106 | -5.218 | 0.07934 | -50.35 | 1551.0 | 0.99997 |
| T2 | 40 | -3.701 | -6.813 | 0.06989 | -56.26 | 1700.2 | 0.99998 |
| T2 | 50 | -5.237 | -8.349 | 0.06227 | -61.03 | 1653.5 | 0.99997 |
| T2 | 60 | -6.773 | -9.885 | 0.05695 | -64.36 | 1690.1 | 0.99998 |
| T3 | 0 | 3.176 | 0.000 | 0.15893 | 0.00 | 227.3 | 0.99993 |
| T3 | 10 | 1.280 | -1.896 | 0.10547 | -33.64 | 267.1 | 0.99968 |
| T3 | 20 | -0.357 | -3.533 | 0.09198 | -42.12 | 1434.9 | 0.99993 |
| T3 | 30 | -1.946 | -5.122 | 0.07982 | -49.78 | 1515.4 | 0.99995 |
| T3 | 40 | -3.490 | -6.666 | 0.07133 | -55.12 | 1575.8 | 0.99997 |
| T3 | 50 | -5.014 | -8.190 | 0.06412 | -59.66 | 1604.3 | 0.99998 |
| T3 | 60 | -6.506 | -9.682 | 0.05930 | -62.69 | 1633.4 | 0.99999 |

附表A-1 42条逐器件转移记录；数据来自transfer_parameters.csv。

# 附录B S1-S3、T1-T3逐器件首扫输出参数全表

| 器件 | 剂量 | \|Id\|@10V/A | \|Id\|@20V/A | \|Id\|@30V/A | 30V变化/% | V@1µA/V | 合规起始/V |
|---|---|---|---|---|---|---|---|
| S1 | 0 | 1.805e-10 | 3.885e-10 | 6.235e-10 | 0.00 | 110.0 | 113.0 |
| S1 | 10 | 1.419e-10 | 3.186e-10 | 6.653e-10 | 6.70 | 57.0 | 115.0 |
| S1 | 20 | 1.758e-10 | 3.932e-10 | 8.331e-10 | 33.62 | 55.0 | 116.0 |
| S1 | 30 | 2.412e-10 | 1.490e-09 | 7.726e-09 | 1139.21 | 36.0 | 113.0 |
| S1 | 40 | 3.025e-10 | 2.494e-09 | 1.981e-08 | 3077.96 | 34.0 | 118.0 |
| S1 | 50 | 4.061e-10 | 1.325e-09 | 4.386e-09 | 603.43 | 41.0 | 117.0 |
| S1 | 60 | 1.094e-09 | 2.845e-09 | 1.153e-08 | 1749.29 | 36.0 | 118.0 |
| S2 | 0 | 2.349e-10 | 4.714e-10 | 7.242e-10 | 0.00 | 110.0 | 112.0 |
| S2 | 10 | 1.861e-10 | 5.846e-10 | 1.509e-09 | 108.33 | 57.0 | 113.0 |
| S2 | 20 | 1.903e-10 | 5.065e-10 | 1.214e-09 | 67.69 | 48.0 | 115.0 |
| S2 | 30 | 2.571e-10 | 1.891e-09 | 1.222e-08 | 1588.03 | 35.0 | 112.0 |
| S2 | 40 | 3.212e-10 | 2.826e-09 | 2.442e-08 | 3271.51 | 35.0 | 115.0 |
| S2 | 50 | 5.025e-10 | 2.268e-09 | 1.574e-08 | 2073.19 | 35.0 | 114.0 |
| S2 | 60 | 1.550e-09 | 3.962e-09 | 2.154e-08 | 2874.44 | 35.0 | 116.0 |
| S3 | 0 | 3.279e-10 | 7.655e-10 | 1.251e-09 | 0.00 | 99.0 | 114.0 |
| S3 | 10 | 1.587e-09 | 6.440e-09 | 1.237e-08 | 888.91 | 39.0 | 114.0 |
| S3 | 20 | 1.342e-09 | 1.330e-08 | 4.960e-08 | 3865.92 | 35.0 | 110.0 |
| S3 | 30 | 2.507e-10 | 2.474e-09 | 1.949e-08 | 1458.57 | 35.0 | 115.0 |
| S3 | 40 | 2.813e-10 | 2.040e-09 | 3.039e-08 | 2329.81 | 33.0 | 109.0 |
| S3 | 50 | 4.112e-10 | 2.440e-09 | 4.120e-08 | 3194.36 | 32.0 | 40.0 |
| S3 | 60 | 9.107e-10 | 2.292e-09 | 1.247e-08 | 897.08 | 35.0 | 40.0 |
| T1 | 0 | 7.305e-11 | 1.016e-10 | 1.185e-10 | 0.00 | 92.0 | 95.0 |
| T1 | 10 | 7.908e-11 | 1.148e-10 | 1.370e-10 | 15.65 | 98.0 | 100.0 |
| T1 | 20 | 1.287e-10 | 1.704e-10 | 2.007e-10 | 69.38 | 105.0 | 106.0 |
| T1 | 30 | 1.273e-10 | 1.783e-10 | 2.300e-10 | 94.09 | 107.0 | 108.0 |
| T1 | 40 | 7.907e-11 | 1.120e-10 | 1.592e-10 | 34.40 | 107.0 | 108.0 |
| T1 | 50 | 8.107e-11 | 1.262e-10 | 1.799e-10 | 51.88 | 107.0 | 108.0 |
| T1 | 60 | 8.170e-11 | 1.357e-10 | 2.046e-10 | 72.71 | 108.0 | 108.0 |
| T2 | 0 | 8.204e-11 | 1.046e-10 | 1.252e-10 | 0.00 | 94.0 | 95.0 |
| T2 | 10 | 7.445e-11 | 1.082e-10 | 1.327e-10 | 5.96 | 99.0 | 101.0 |
| T2 | 20 | 7.305e-11 | 1.151e-10 | 1.387e-10 | 10.77 | 105.0 | 107.0 |
| T2 | 30 | 7.258e-11 | 1.145e-10 | 1.434e-10 | 14.50 | 108.0 | 108.0 |
| T2 | 40 | 9.468e-11 | 1.361e-10 | 1.777e-10 | 41.90 | 108.0 | 109.0 |
| T2 | 50 | 9.159e-11 | 1.321e-10 | 1.915e-10 | 52.94 | 108.0 | 109.0 |
| T2 | 60 | 7.945e-11 | 1.464e-10 | 1.990e-10 | 58.87 | 109.0 | 109.0 |
| T3 | 0 | 7.127e-11 | 9.672e-11 | 1.219e-10 | 0.00 | 92.0 | 95.0 |
| T3 | 10 | 7.526e-11 | 9.859e-11 | 1.200e-10 | -1.57 | 98.0 | 100.0 |
| T3 | 20 | 7.225e-11 | 1.058e-10 | 1.237e-10 | 1.46 | 104.0 | 106.0 |
| T3 | 30 | 6.648e-11 | 1.067e-10 | 1.308e-10 | 7.34 | 107.0 | 107.0 |
| T3 | 40 | 7.364e-11 | 1.110e-10 | 1.460e-10 | 19.80 | 107.0 | 107.0 |
| T3 | 50 | 7.008e-11 | 1.133e-10 | 1.679e-10 | 37.76 | 107.0 | 107.0 |
| T3 | 60 | 7.712e-11 | 1.298e-10 | 1.815e-10 | 48.93 | 107.0 | 107.0 |

附表B-1 42条逐器件首扫输出记录；13条复扫另见表2-2。

# 附录C T模型、剂量映射与正式证据索引

| 项目 | 内容 | 状态 |
|---|---|---|
| 不可变上游 | Trench VDMOS.gzp；SHA-256 4d09...68bf | SUPPORTED |
| 固定参数 | P-body 1.33×10¹⁷ cm⁻³；AreaFactor=30335；300 K | SUPPORTED |
| 剂量映射 | Not/Nit低参数单调函数；七剂量共同标定 | QUALIFIED calibration |
| 运行策略 | VM原子单核lease；sdevice --threads 1；串行依赖链 | SUPPORTED |
| 正式曲线 | 真实VM SVisual；不删点/不平滑/不插值/不补零 | SUPPORTED |
| D30 | 15.6-30 V；17点；CSV SHA-256 3a14...361 | QUALIFIED_PARTIAL |
| D40 | 0.003-30 V；163点；6负点；CSV SHA-256 8b93...ba9 | QUALIFIED |
| V@1µA仿真 | 无完整有效代理 | BLOCKED |

# 附录D 失败、重试与排除结果时间线

| 阶段 | 保留事实 | 正式处理 |
|---|---|---|
| 旧D30无雪崩输出 | 在13.722894891 V附近数值失败 | HISTORICAL，不进入当前曲线 |
| D30 staged retry | 失败证据与runner错误保留 | HISTORICAL |
| D30 checkpoint续跑 | exit 0；仅15.6-30 V | 当前QUALIFIED_PARTIAL |
| D40 direct旧run | 被reboot-retry替代 | SUPERSEDED |
| D40 reboot-retry | 163点；6个负点复现 | PROMOTABLE且带异常限定 |
| 高场/IIC尝试 | 不同偏压与收敛状态分别保留 | 不与实验V@1µA混同 |

# 附录E 照片、截图与图表来源清单

| 报告资产 | 只读来源 | SHA-256 | 证据等级 |
|---|---|---|---|
| route.png | E:\仿真数据处理\deliverables\07_presentation\素材\新版PPT素材库_20260722\05_文献与实验现场\背景与机制图\03_本项目研究闭环_原创.png | c86280de7d4754dc6723c45e6bf7e2c9ae0ee504e766943a6224bbc66b6b8b4b | SUPPORTED/QUALIFIED（见图注） |
| site_irradiator.jpg | E:\仿真数据处理\deliverables\07_presentation\素材\新版PPT素材库_20260722\05_文献与实验现场\现场照片\辐照台.jpg | 29156f31d8a94eda2e7729ccaf8cd566cf97fa5a1dd470480ed7055dbb13110a | SUPPORTED |
| site_room.jpg | E:\仿真数据处理\deliverables\07_presentation\素材\新版PPT素材库_20260722\05_文献与实验现场\现场照片\辐照室外面.jpg | f9acecc8cfc97f263b4cb2c2c0ccca4e4738da64b7dd4d25d7ce810727935c8e | SUPPORTED |
| site_source.jpg | E:\仿真数据处理\deliverables\07_presentation\素材\新版PPT素材库_20260722\05_文献与实验现场\现场照片\重水和内部钴源.jpg | 610ff9274acf924e11246cbb31dcdccc4130db879741aa4ae1d83800379f6359 | SUPPORTED |
| transfer_linear_S.png | E:\仿真数据处理\deliverables\03_figures\png\transfer_linear_S.png | 4c0ad0c37ad35b35c4d1284842fa6480c98df7b387893c74bcced9f7f0fd6082 | SUPPORTED/QUALIFIED（见图注） |
| transfer_semilog_S.png | E:\仿真数据处理\deliverables\03_figures\png\transfer_semilog_S.png | 6fe00d180d7655e7b9f854d56916b29d6f0d44db627982f68f571aa264d20654 | SUPPORTED/QUALIFIED（见图注） |
| output_semilog_S.png | E:\仿真数据处理\deliverables\03_figures\png\output_semilog_S.png | 4cd8f1dfee27b87b0d17eeb8f0387e1cad0e7ec54d627eb8a46e073aff4c54a8 | SUPPORTED/QUALIFIED（见图注） |
| transfer_linear_T.png | E:\仿真数据处理\deliverables\03_figures\png\transfer_linear_T.png | 77569daf922408e71f04d6e5c1841dc556a1c97dbff372c3d44df839a873fb4d | SUPPORTED/QUALIFIED（见图注） |
| transfer_semilog_T.png | E:\仿真数据处理\deliverables\03_figures\png\transfer_semilog_T.png | 02ff90011bbfb19e7204c71cad56e35aaa9885d89e2cb51007f0aaae660bfaa9 | SUPPORTED/QUALIFIED（见图注） |
| output_semilog_T.png | E:\仿真数据处理\deliverables\03_figures\png\output_semilog_T.png | f4c418a8353a29218265333247c3237f20b375edb00fd8592e6c30728d4c5317 | SUPPORTED/QUALIFIED（见图注） |
| threshold_shift.png | E:\仿真数据处理\deliverables\03_figures\png\threshold_shift.png | c21f61f7abc14a715b1007c91e8f8d88a0b9d98d11c4ed0d905b14294b904967 | SUPPORTED/QUALIFIED（见图注） |
| gm_change.png | E:\仿真数据处理\deliverables\03_figures\png\gm_change.png | 98e74e3f7b08475af3d3ef83b64e24f9545e046f876c72a49931567bc4e9d9cb | SUPPORTED/QUALIFIED（见图注） |
| subthreshold_swing.png | E:\仿真数据处理\deliverables\03_figures\png\subthreshold_swing.png | b9f3e50cf1c75143d615ecfcfcec58fed8204526800795789a7f27ec4bbaa3da | SUPPORTED/QUALIFIED（见图注） |
| output_current_30v.png | E:\仿真数据处理\deliverables\03_figures\png\output_current_30v.png | e2dc11cccfc208a0260a28078503b86e48cfb3c0365d0186f944e77c40b6a041 | SUPPORTED/QUALIFIED（见图注） |
| voltage_at_1ua.png | E:\仿真数据处理\deliverables\03_figures\png\voltage_at_1ua.png | db359c96f29b22d6494ed0b224dfa82fd91d4853fafe4b509fa078b2696f9667 | SUPPORTED/QUALIFIED（见图注） |
| stress_recovery_30v.png | E:\仿真数据处理\deliverables\03_figures\png\stress_recovery_30v.png | bca9f7f9c5dd24e5d2f0824bc84857d06bce8e826fdadea8f7fb0b9e1695593e | SUPPORTED/QUALIFIED（见图注） |
| sim_structure_mesh.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\simulation\structure_mesh.png | a61acb7b154516f381b70b56ee0e4df770b5f6154139114b48d8a1fbcc5691c5 | SUPPORTED |
| sim_transfer_semilog.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\comparison\comparison_transfer_semilog_T.png | 585c738d6f9a377b8d0dca53e0fc3a66514bca9b9e7fa98994d2f44834fa4e71 | SUPPORTED/QUALIFIED（见图注） |
| sim_transfer_metrics.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\comparison\comparison_transfer_metrics_T.png | dc570fb6f323a9fb18a9852c434357d47156ef7cfd9bb9f57f4dde91b64fcde2 | SUPPORTED/QUALIFIED（见图注） |
| sim_output_semilog.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\comparison\comparison_output_semilog_T.png | f0642d72ac5cedf8fb1799e26b8ef6c2e0fe2b5b7405907fa399dfbb6a94bd6b | SUPPORTED/QUALIFIED（见图注） |
| sim_id30.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\comparison\comparison_id30_T.png | 81ba9b78c6c58e6717671e392867cef96f6ef8cbaf7b9762592e2cc91d332677 | SUPPORTED/QUALIFIED（见图注） |
| sim_high_voltage_context.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\comparison\comparison_high_voltage_context_T.png | e028e7389e4ad0cc7515b0be998694d4b4b5948067fec9d3b6279c77f5013d38 | SUPPORTED/QUALIFIED（见图注） |
| sim_field_0.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\simulation\electric_field_0krad.png | c79a4812566bb327c4255d91320c6c2003dda2f9c301ac538ea4852ceb234f2a | SUPPORTED |
| sim_field_60.png | E:\仿真数据处理\deliverables\06_simulation\06_report_materials\figures_T\simulation\electric_field_60krad.png | 0fb195488e3a47472a9f4dea11b412fb8acee1825666a65f9cab8b78c2d1387f | SUPPORTED |

所有 assets 均为源图复制件或为报告服务的派生资产；源图未被修改。实验图回溯至 deliverables/02_data 与 03_figures；仿真图回溯至 deliverables/06_simulation 正式证据。