# 图注（T 器件 Sentaurus TID 验证）

1. **transfer_semilog_T**：T 器件 0–60 krad(Si) 转移特性半对数图；正式曲线来自 Sentaurus PLT，显示负向阈值漂移和亚阈值区变化。
2. **output_semilog_T**：$V_{GS}=-20$ V、无雪崩反馈的预击穿输出电流。D30 新 clone 为 **QUALIFIED_PARTIAL，15.6–30 V**，不得解释为完整 0.003–30 V；D40 为 PROMOTABLE，保留 6 个低压负点并限定为复现数值异常。
3. **output_current_30v_T**：30 V 输出电流对比。D30 只使用新 clone 的 30 V 当前点，不补齐低压区；不把 $I_D@30$ 当作 V@1uA。
4. **threshold_voltage_T**：Savitzky–Golay 切线法阈值电压随剂量变化。
5. **threshold_shift_T**：阈值漂移；七剂量标定 $\Delta V_{th}$ RMSE=0.0771 V。
6. **gm_change_T**：最大跨导相对变化；七剂量 RMSE=5.97 个百分点。
7. **subthreshold_swing_T**：亚阈值摆幅；60 krad 仿真/实测为 892/1674 mV/dec，差异标示模型边界。
8. **voltage_at_1ua_T**：实测 V@1uA；仿真代理未获得，明确标注不可比较。
9. **structure_mesh**：固定二维沟槽结构和网格，来自真实 VM SVisual。
10. **electric_field_0krad / electric_field_60krad**：实际 TDR 的预击穿终态电场导出。

D30 的所有图例和图注均使用 `QUALIFIED/PARTIAL: 15.6-30 V only`，Origin 图与 SVisual 正式图严格分开标识。