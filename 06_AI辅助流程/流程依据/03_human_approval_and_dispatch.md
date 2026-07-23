# 人工审批与精确下发

上级：[通用治理规范](01_general_governance.md)
依赖：`simulation/config/supervision/ai_supervision.schema.json`、对应 campaign config

## Proposal

AI proposal 必须包含候选参数、物理理由、备选方案、使用与排除的 run IDs、证据 hash、各代理意见、预算、允许的数值策略以及停止条件。proposal 的状态固定为 `HUMAN_APPROVAL_PENDING`，不得作为执行输入。

## Decision record

人工批准记录至少包含：

- `decision_id`、批准人、批准与过期时间；
- `campaign_id`、`round_id`、`config_sha256`；
- 候选 ID 与完整参数值；
- 允许的 deck、数值策略、最大候选数和 recovery/retry 范围；
- 证据 hashes 和被拒绝的备选方案。

批准记录是 append-only。只要 `campaign_id`、`round_id`、config/evidence hashes、候选白名单、资源预算和允许动作均未变化，单一执行代理可在该 decision 有效期内下发白名单候选，无需逐项重复审批。新增候选、改变参数或 hash、扩大目标/预算/候选生成边界、增加未批准的 retry/recovery/refinement、进入新 round 或 decision 过期时，必须重新审批。

## 下发门

执行代理必须 fail-closed 检查：

1. decision 为 `APPROVED` 且未过期；
2. decision 的 campaign、round、候选白名单与命令一致；
3. config、deck 和证据 hash 与批准时一致；
4. GZP 或设备上游模型 hash 正确；
5. VM lease probe 可用，没有第二个不受控 dispatcher；
6. local/remote campaign root 显式提供，不使用旧默认路径。

执行只允许批准的候选和动作。同一有效 campaign authorization 的锁定白名单内无需逐候选重复 decision；任何越界请求必须 fail-closed 返回 `HUMAN_APPROVAL_PENDING`。默认不传 `-RetryFailed`；重试与 recovery 必须作为批准范围内的独立 work item。

成功下发后，执行权立即与观察权分离：父会话派遣只读异步监控代理，按[代理角色与状态机](02_agent_roles_and_state_machine.md)核对本地 manifest、远端进程和 atomic lease。监控事件不能授权新 deck、重试或 dispatcher。

## Schema 边界

现有 `ai_supervision.schema.json` 是 T v1 兼容契约，其中 `trench_tid_*`、`epi_h_um` 和 `epi_doping_cm3` 不是设备无关字段。未来 S 适配不得通过空值或复用 T 字段绕过设备 contract。

## 非执行示例

本目录 Markdown 模板和将来的 `*.example.json` 均必须标注 `EXAMPLE_ONLY_NOT_APPROVED_NOT_EXECUTABLE`。执行器只能读取指定 campaign 下经人工批准、hash 锁定的 decision record。