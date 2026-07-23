# T 器件总电离剂量（TID）Sentaurus 仿真技术验证报告

**活动标识：** `trench_tid_20260715_231741`  
**对象：** T 组二维沟槽器件，300 K，0–60 krad(Si)  
**报告性质：** 标定范围内的可追溯技术验证，不是外推预测，也不宣称普适辐照物理定律。

## 摘要

**目的。** 本报告验证固定二维沟槽器件模型在总电离剂量（TID）下对 T 组转移特性和无雪崩预击穿输出特性的可复现范围，并明确数值求解边界。

**方法。** 上游采用不可变 `Trench VDMOS.gzp`，固定结构、P-body 掺杂、AreaFactor、温度、陷阱形状及捕获参数；剂量只通过已记录的氧化层固定电荷和界面陷阱剂量函数变化。每个 SDevice 使用 VM 侧原子单核租约并执行 `sdevice --threads 1`。正式曲线由真实 VM Sentaurus Visual 提取，保留原始点，不删点、不平滑、不插值、不补零。定量 Vth/gm/SS 沿用 `analysis_config.json` 的 Savitzky–Golay 与滑动窗口方法。

**结果。** 七剂量转移标定的 $\Delta V_{th}$ RMSE 为 0.0771 V，gm 变化 RMSE 为 5.97 个百分点；60 krad 的 SS 仿真/实测为 892/1674 mV/dec，残差仍是模型边界。D30 新 clone 从 checkpoint_14 独立续跑并 exit 0，但其 SVisual PLT 仅覆盖 **15.6–30 V、17 点**，因此当前分类为 **QUALIFIED_PARTIAL**；不得补齐 0.003–15.6 V，也不得拼接旧曲线。D30 当前 30 V 电流为 $9.49939128786\times10^{-9}$ A。D40 新 reboot-retry 为 **PROMOTABLE**，163 点覆盖 0.003–30 V，30 V 电流为 $1.37863878805\times10^{-8}$ A，6 个低压负点作为可复现数值异常保留。

**局限。** D30 低压段仍缺失；D40 异常不能解释为已证实物理转变；V@1uA 仿真代理未获得，不能用 $I_D@30$ 或 IIC 电压替代；S 组和应力恢复仿真不适用。Origin COM 叠加资产与 SVisual 正式图分开标识。

**关键词：** TID；Sentaurus；沟槽器件；阈值电压；界面陷阱；可追溯性

## 1 研究范围与证据规则

本次闭环只讨论 T 组、300 K 和 0、10、20、30、40、50、60 krad(Si)。S 组仿真及应力恢复仿真在本活动中不适用。正式仿真证据必须同时具有实际 deck、PLT、solver log/stdout、单核 lease 记录、终态偏压检查、解析 CSV 与哈希；文件关系见 `01_provenance/current_output_provenance.json`、`evidence_map.json` 和交付 manifest。

报告区分四类状态：`current` 是本轮选定的正式输入；`QUALIFIED_PARTIAL` 是有明确覆盖区间但不完整的结果；`HISTORICAL` 是保留但不进入当前正式曲线的旧尝试；`SUPERSEDED` 表示被新结果替代。老 D30 PID 12620 属于排除对象，本报告不等待、不终止、不纳入任何图。

## 2 模型、配置与运行约束

上游 `Trench VDMOS.gzp` SHA-256 为 `4d09d17b88e9cb0fd0783875f9ec3446795d8b6bd3ba3b136d1bacb73da368bf`，本轮前后哈希一致。模型固定二维沟槽结构、P-body 掺杂 $1.33\times10^{17}\ \mathrm{cm^{-3}}$、`AreaFactor=30335`、300 K、转移 $V_{DS}=0.1$ V；输出曲线使用 $V_{GS}=-20$ V 和无雪崩反馈。陷阱形状为解包 deck 可追溯的均匀 Acceptor 设定。

每个 SDevice 通过 VM 原子租约分配一个 CPU，并由 affinity 验证确认；运行命令为 `sdevice --threads 1 --exit-on-failure`。高陷阱节点保持 Poisson/稳态初始化和串行 bias ramp。真实 VM SVisual 用于 PLT 提取，不把 Origin COM 资产冒充 SVisual。

## 3 剂量参数与转移特性

本活动采用低参数单调映射：

$$N_{ot}(D)=3.0\times10^{10}+4.96\times10^{12}(D/60)^{0.87}\ \mathrm{cm^{-2}},$$

$$N_{it}(D)=1.4\times10^{11}+4.0\times10^{12}(D/60)^{0.70}\ \mathrm{cm^{-2}}.$$

七个剂量点共同参与标定，因此以下误差是范围内标定质量，不是独立盲测误差。

| 指标 | 结果 |
|---|---:|
| 七剂量 $\Delta V_{th}$ RMSE | 0.0771 V |
| 60 krad $\Delta V_{th}$ 误差 | 0.00177 V |
| 七剂量 gm 变化 RMSE | 5.97 个百分点 |
| 60 krad gm（仿真/实测） | −63.22% / −61.21% |
| 60 krad SS（仿真/实测） | 892 / 1674 mV/dec |

A–I 扫描显示：增加同一均匀 Acceptor 陷阱可以提高 SS，但会过度压低 gm；因此本报告不通过无约束增加陷阱来掩盖 SS 残差。

![图 1：T 组转移特性和剂量演变，正式 SVisual 图](../04_figures/transfer_semilog_T.png)

## 4 输出曲线当前晋级结果

### 4.1 D30：新 clone 的 QUALIFIED_PARTIAL

D30 新 run 为 `output_repair_d30_clone_from14__20260716T095920119Z__22a327fb`，从 checkpoint_14 复制工程后独立续跑，`exit_code=0`、CPU 2、`sdevice --threads 1`，solver log 含 Good Bye，lease acquisition/release 与 affinity 均有记录。其真实 VM SVisual 提取 `output_d30.csv` 只有 17 个原始点，首点 15.6 V，末点 30 V，横坐标单调且无 NaN；30 V 电流为 $9.49939128786\times10^{-9}$ A。

因此 D30 当前状态为 **QUALIFIED_PARTIAL（15.6–30 V）**。15.6 V 以下不是本次 clone PLT 的观测数据，不进行补点、插值、平滑、零填充或与任何历史曲线拼接。旧的 D30 失败 run `output_final_noaval_d30_to30__20260715T214133175Z__203472cf` 保留为 `HISTORICAL`，其 13.722894891 V 终止证据不进入当前 D30 曲线。图例和图注均标明 D30 的 15.6–30 V 覆盖范围。

### 4.2 D40：PROMOTABLE，但保留数值异常

D40 当前 run 为 `output_repair_d40_direct_rebootretry__20260716T023543900Z__1bac4524`。SVisual 提取 163 点，覆盖 0.003–30 V，首末点通过 gate；30 V 电流为 $1.37863878805\times10^{-8}$ A。低压区有 6 个负点，且该现象在新 run 中复现，因此分类为 **PROMOTABLE / REPRODUCED_NUMERICAL_ANOMALY_QUALIFIED**。所有带符号原始点保留；半对数显示只使用可追溯的 `abs(Id)` 派生列，不将负点改写为正物理电流。

![图 2：无雪崩预击穿输出半对数图；D30 标为 15.6–30 V partial，D40 保留异常点](../04_figures/output_semilog_T.png)

![图 3：30 V 输出电流；D30 只对当前 30 V 点显示，低压缺口不补齐](../04_figures/output_current_30v_T.png)

## 5 Origin 原始曲线叠加

Origin COM 脚本 `scripts/build_origin_t_output_overlay.py` 读取 21 条 T1/T2/T3 实测原始曲线和 7 条当前 SDevice 原始曲线，共 28 条。全剂量线性叠加图和半对数叠加图各 28 条；另有 7 张逐剂量四曲线图。Origin 工作表保留原始有符号 $I_D$，半对数列明确由 `abs(signed_id)` 派生；不均值化、不重采样、不删点、不平滑、不插值。颜色表示剂量，线型表示 T1/T2/T3/SDevice。

D30 SDevice 曲线在 Origin 图例中明确标记 `QUALIFIED/PARTIAL: 15.6-30 V only`，Origin manifest 记录其 current run ID、CSV 哈希、覆盖区间和状态。Origin OPJU、PNG、PDF、EMF 仅是叠加/展示资产，不替代正式 SVisual 证据；`origin_qa.json` 为 PASS。

## 6 高场指标的边界

IIC 和 V@1uA 是不同指标。IIC 只在相应偏压和求解收敛条件下解释；V@1uA 是实测定义的电流代理。当前没有完整有效的 V@1uA 仿真曲线，不能以 IIC 电压或 $I_D@30$ 替代。30 V 电流可作为输出曲线的采样点，但不应被写成 V@1uA。

| 口径 | 当前结论 |
|---|---|
| D30 no-avalanche output | QUALIFIED_PARTIAL，15.6–30 V，17 点 |
| D40 no-avalanche output | PROMOTABLE，0.003–30 V，163 点 |
| D40 低压异常 | 6 个负点，复现并限定为数值异常；不作物理机制断言 |
| V@1uA 仿真代理 | 未获得，BLOCKED / 不可比较 |
| S 组、应力恢复 | 本 T-only campaign 不适用 |

## 7 不确定性、历史证据与对抗性审查

主要不确定性来自三个方面。第一，七剂量共同参与标定，RMSE 不能代表外推精度。第二，均匀 Acceptor 陷阱模型无法同时解释 SS 和 gm 的全部退化，不能把残差包装为已解决。第三，D30 当前数据覆盖不足，D40 的负低压点虽可复现，但数值复现不等于物理机制确认。

对抗性审查重点检查：是否把 D30 partial 写成完整 0.003–30 V；是否把旧 D30 失败曲线拼入新 clone；是否把 D40 负点删掉或平滑；是否把 Origin 图称为 SVisual；是否把 $I_D@30$ 写成 V@1uA；是否把 historical/superseded 结果当 current。上述风险均在 claim audit 和 adversarial review 中逐项记录。

## 8 结论与后续边界

本闭环支持以下谨慎结论：在当前 T 器件、300 K、0–60 krad(Si) 标定范围内，低参数 Dose-to-$N_{ot}/N_{it}$ 映射能够复现阈值负移和 gm 衰减的主要趋势；D40 新结果可用于当前输出曲线，但需携带数值异常限定；D30 新 clone 证明了 15.6–30 V 的独立续跑结果，却没有证明 0.003–15.6 V 段，因此只能作为 QUALIFIED_PARTIAL。

不支持的结论包括：D30 已获得完整 0.003–30 V 曲线、D40 异常是已证实的物理跃迁、V@1uA 已由仿真得到、S 组或应力恢复已完成。未来若需补齐 D30，必须产生新的独立低压 PLT 和完整证据链，不得回填或拼接本轮缺失区间。

## 附录：主要证据路径

- current provenance：`../01_provenance/current_output_provenance.json`
- D30 current CSV：`../02_data/svisual_extracted_curves/output_d30.csv`
- D40 current CSV：`../02_data/svisual_extracted_curves/output_d40.csv`
- Origin manifest/QA：`../07_origin/origin_overlay_manifest.json`、`../07_origin/origin_qa.json`
- claim audit：`claim_audit.json`
- evidence map：`evidence_map.json`
- 报告四格式：本目录 MD/TEX/PDF/DOCX

**数据可用性：** 紧凑派生数据、正式 deck、压缩证据、验证记录、图和哈希清单随交付提供；大型 VM 原始运行保留于忽略的 `local_runtime/tcad_runs/`。  
**AI 使用：** 自动化工具用于格式转换、资产编排和一致性检查；数值结论均回溯至实际测量派生数据或真实 VM Sentaurus 证据。