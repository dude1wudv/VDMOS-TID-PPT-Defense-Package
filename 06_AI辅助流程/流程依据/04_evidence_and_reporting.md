# 证据复核与上级汇报

上级：[通用治理规范](01_general_governance.md)
依赖：设备手册、对应 validator/scorer、campaign config

## 数值复核

至少检查：solver lifecycle、Newton/RHS/MinStep、最终端偏压、收敛点、checkpoint、compliance/安全停止、`sdevice --threads 1`、lease 获取/释放和 affinity。数值失败点只表示该运行无可用数据，不能用于推断物理方向。

## 证据复核

一条可比较探索曲线至少需要实际 deck、mesh、run manifest、solver stdout/stderr、PLT、真实 VM SVisual CSV、validation、score 和输入输出 SHA-256。正式曲线还必须满足设备适配的 formal promotion 门。

缺失关键证据时状态保持 `EVIDENCE_PENDING`。不得用 IIC、图片像素、插值或外推填补未得到的输出曲线。

## 上报触发条件

以下任一情况向父会话/人工批准人汇报：

- 出现符合设备适配门的趋势候选；
- 出现 partial、right-censored 或 numerical no-data；
- 固定轮次全部完成且无活动租约；
- 异步监控发现 dispatcher/runner 意外退出，或本地 manifest、远端进程与 atomic lease 状态冲突；
- 同一区域重复数值失败或没有可辩护的参数方向；
- 上游/config/deck/mesh hash、偏置、lease/affinity 或安全条件异常；
- 参数经理结论冲突、推荐对删点敏感或需要扩大物理边界；
- 达到批准的轮数、时间或计算预算。

## 上报内容

- campaign、round、decision、候选和设备组；
- 状态分类与关键曲线特征；
- run、solver、lease、SVisual、validation、score 和 hash 证据；
- 所有失败/recovery 尝试；
- 各代理建议、分歧和被拒绝方案；
- 人工批准范围、剩余不确定性和下一步选项。

探索结果必须明确 `formal_valid=false`。只有设备专属正式门禁和人工晋级均通过后，才可建议进入正式多剂量运行或报告图件。