# 逐页内容矩阵

- 总页数：44
- 30/45/60 分钟路线由 KEEP/SKIP 字段控制。

|页|章节|动作标题|证据|30|45|60|时长(s)|
|---:|---|---|---|---|---|---|---:|
|1|封面|S/T 组 VDMOS 总电离剂量实验与 T 器件 TCAD 验证|SUPPORTED|KEEP|KEEP|KEEP|30|
|2|导航|同一套 44 页材料支持 30、45 与 60 分钟三条路线|SUPPORTED|KEEP|KEEP|KEEP|60|
|3|背景与问题|TID 通过氧化层与界面陷阱影响阈值、跨导、亚阈区和高压响应|QUALIFIED|KEEP|KEEP|KEEP|70|
|4|背景与问题|文献提供机制背景，本项目聚焦六只器件的同口径纵向证据|QUALIFIED|SKIP|KEEP|KEEP|60|
|5|背景与问题|项目闭环从原始测量延伸到可追溯的 T-only Sentaurus 证据|SUPPORTED|KEEP|KEEP|KEEP|60|
|6|样品与方法|S/T 各 3 只器件在七个剂量点持续纵向跟踪|SUPPORTED|KEEP|KEEP|KEEP|70|
|7|样品与方法|辐照与测试时序固定，剂量率不从 198 s 记录自行换算|SUPPORTED|SKIP|KEEP|KEEP|80|
|8|样品与方法|原始表经清洗、统一参数算法与质控后进入图表和仿真比较|SUPPORTED|KEEP|KEEP|KEEP|80|
|9|实验转移特性|六只器件的七剂量曲线共同显示阈值负移与开启能力下降|SUPPORTED|KEEP|KEEP|KEEP|90|
|10|实验转移特性|S1：七剂量转移曲线保留完整扫描范围与低电流细节|SUPPORTED|KEEP|KEEP|KEEP|45|
|11|实验转移特性|S2：七剂量转移曲线保留完整扫描范围与低电流细节|SUPPORTED|SKIP|SKIP|KEEP|45|
|12|实验转移特性|S3：七剂量转移曲线保留完整扫描范围与低电流细节|SUPPORTED|SKIP|SKIP|KEEP|45|
|13|实验转移特性|T1：七剂量转移曲线保留完整扫描范围与低电流细节|SUPPORTED|KEEP|KEEP|KEEP|45|
|14|实验转移特性|T2：七剂量转移曲线保留完整扫描范围与低电流细节|SUPPORTED|SKIP|SKIP|KEEP|45|
|15|实验转移特性|T3：七剂量转移曲线保留完整扫描范围与低电流细节|SUPPORTED|SKIP|SKIP|KEEP|45|
|16|实验转移特性|60 krad：两组 ΔVth 负移 6–10 V，gm 均下降约 60%|SUPPORTED|KEEP|KEEP|KEEP|100|
|17|实验输出特性|输出结果的主线是 Id@30V、曲线形态与器件级异常|SUPPORTED|KEEP|KEEP|KEEP|30|
|18|实验输出特性|六只器件的七剂量输出响应呈现明显组内差异与非单调细节|SUPPORTED|KEEP|KEEP|KEEP|80|
|19|实验输出特性|S1：七剂量输出曲线保留拐点、非单调与合规限流段|SUPPORTED|KEEP|KEEP|KEEP|45|
|20|实验输出特性|S2：七剂量输出曲线保留拐点、非单调与合规限流段|SUPPORTED|SKIP|KEEP|KEEP|45|
|21|实验输出特性|S3：七剂量输出曲线保留拐点、非单调与合规限流段|SUPPORTED|SKIP|KEEP|KEEP|45|
|22|实验输出特性|T1：七剂量输出曲线保留拐点、非单调与合规限流段|SUPPORTED|KEEP|KEEP|KEEP|45|
|23|实验输出特性|T2：七剂量输出曲线保留拐点、非单调与合规限流段|SUPPORTED|SKIP|KEEP|KEEP|45|
|24|实验输出特性|T3：七剂量输出曲线保留拐点、非单调与合规限流段|SUPPORTED|SKIP|KEEP|KEEP|45|
|25|实验输出特性|Id@30V 与实验 V@1µA 给出两种不同的剂量响应视角|SUPPORTED|KEEP|KEEP|KEEP|100|
|26|S 组复扫|13 条 S 组后续扫描的 30 V 漏电均低于同剂量首扫|SUPPORTED|KEEP|KEEP|KEEP|80|
|27|S 组复扫|S3 60 krad 案例显示全范围与 40–70 V 局部均发生扫描后降低|QUALIFIED|KEEP|KEEP|KEEP|70|
|28|T 模型与方法|T 器件二维结构与网格固定，剂量只改变可追溯陷阱参数|SUPPORTED|KEEP|KEEP|KEEP|80|
|29|T 模型与方法|低参数 Dose-to-Not/Nit 映射覆盖全部七剂量共同标定点|SUPPORTED|KEEP|KEEP|KEEP|80|
|30|T 转移实验—仿真|T 转移全剂量：复现阈值负移，开启区仍有量值差异|SUPPORTED|KEEP|KEEP|KEEP|100|
|31|T 转移实验—仿真|ΔVth 与 gm 在共同标定范围内达到可复现的定量一致性|SUPPORTED|KEEP|KEEP|KEEP|100|
|32|T 转移实验—仿真|均匀 Acceptor 陷阱无法同时消除 SS 与 gm 的全部残差|QUALIFIED|SKIP|KEEP|KEEP|80|
|33|T 输出、高场与 IIC|无雪崩预击穿输出只能作限定趋势比较，不能称为 BV 拟合|QUALIFIED|KEEP|KEEP|KEEP|100|
|34|T 输出、高场与 IIC|Origin 叠加保留 21 条实测与 7 条 SDevice 原始曲线|QUALIFIED|SKIP|KEEP|KEEP|90|
|35|T 输出、高场与 IIC|IIC 只在当前模型、偏压路径与收敛判据下条件化解释|QUALIFIED|KEEP|KEEP|KEEP|100|
|36|T 输出、高场与 IIC|0 与 60 krad 的终态电场分布可视化来自真实 VM SVisual|QUALIFIED|SKIP|KEEP|KEEP|100|
|37|S 仿真状态|S 组正式剂量标定仿真尚未纳入本版|BLOCKED|KEEP|KEEP|KEEP|45|
|38|综合讨论|实验、文献与 T 模型共同支持一条有边界的解释链|QUALIFIED|KEEP|KEEP|KEEP|100|
|39|成果与能力|项目已形成从 22,627 个原始曲线点到正式仿真证据的完整资产链|SUPPORTED|KEEP|KEEP|KEEP|90|
|40|结论|本批器件的共同转移退化已确认，输出响应与历史效应需要分口径解释|SUPPORTED|KEEP|KEEP|KEEP|90|
|41|附录|Vth、gm、SS 与输出参数使用统一、可复现的计算口径|SUPPORTED|SKIP|SKIP|KEEP|60|
|42|附录|D30、D40、IIC 与 V@1µA 的状态必须随图携带|QUALIFIED|SKIP|SKIP|KEEP|90|
|43|附录|来源、模板授权与不可变输入在交付前后保持可核查|SUPPORTED|SKIP|SKIP|KEEP|90|
|44|致谢|完整数据、边界可见、结果可追溯|SUPPORTED|KEEP|KEEP|KEEP|30|
