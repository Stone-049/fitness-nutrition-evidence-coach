# 同类 Skill / 项目能力对比

调研日期：2026-10-22。

## 样本项目

### BorisBW/claude-fitness-cn

https://github.com/BorisBW/claude-fitness-cn

定位：数据驱动的 Claude Code 健身教练。

已实现：

- Garmin、Coros、WHOOP、Apple Watch 数据接入
- 睡眠、HRV、静息心率、训练负荷和主观状态
- readiness 评分、HRV 个人基线、ACWR、训练量负荷
- 力量训练与耐力训练双负荷模型
- Markdown/Obsidian 本地记录
- 移动端仪表盘
- 结构化训练计划推送

可借鉴：

- 可解释公式
- 本地优先和数据可导出
- 训练负荷与恢复趋势
- 缺失数据时明确降级，不假装完整

### RiccardoRiccio/Fitness-AI-Trainer

https://github.com/RiccardoRiccio/Fitness-AI-Trainer-With-Automatic-Exercise-Recognition-and-Counting

定位：计算机视觉动作识别与计数。

已实现：

- MediaPipe 姿态估计
- LSTM/BiLSTM 动作分类
- 实时重复计数
- Streamlit 交互界面

可借鉴：

- 用姿态关键点而不是只看单张照片
- 输出动作阶段、计数和置信度
- 只做动作识别，不夸大医疗判断

### Gym-Exercise-Posture-Analysis

https://github.com/zubaerturjo/Gym-Exercise-Posture-Analysis

定位：基于姿态关键点的健身动作/体态分析。

可借鉴：

- 关键点角度、轨迹和时间序列
- 动作质量反馈
- 视觉结果需要人工/规则复核

### Fitness-AQA / Fitness-OS

https://github.com/ParitoshParmar/Fitness-AQA

https://github.com/liuchuan01/Fitness-OS

可借鉴：

- 运动知识问答
- 本地规则校验
- 训练记录先验证再写入
- AI 草稿不能直接成为正式记录

## 我们的相对实现路线

### P0 已完成

- 教练人设
- 成人同意与隐私门槛
- 身体图像分析规范
- 训练/营养知识库
- 题库校验与盲测评分

### P1 近期

- readiness 评分
- volume load 与 sRPE 训练负荷
- 训练日志导入和趋势报告
- 图像分析前置检查脚本

### P2 中期

- Garmin/Coros/WHOOP/Apple 数据适配
- 本地 Markdown/Obsidian 记录
- 周复盘和自适应计划

### P3 后期

- MediaPipe/OpenPose 动作关键点
- 视频动作分类与计数
- 仅在有专业审核时提供动作质量反馈

## 结论

同类项目的优势是数据接入、实时姿态识别、训练负荷和本地记录。我们的优势是证据边界、普通人的可执行建议、图像隐私规则和题库质量校验。最佳实现不是复制它们，而是把“知识、教练、图像、数据记录”拆成可验证模块。


以上项目仅作功能研究和架构比较，未复制其代码或数据。
