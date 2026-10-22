# Fitness Nutrition Evidence Coach

一个面向健康普通人的循证健身与运动营养 Skill 草稿，包含训练、营养、安全、课程笔记、题库校验和盲测评分脚本。

## 目录

- SKILL.md：Skill 主规范和强制工作流
- references/：证据、训练、营养、安全、课程和错误预防资料
- scripts/：题库校验、答案键拆分、盲测评分
- tests/：最小回归样例

## 运行校验

    python scripts/validate_question_bank.py --questions tests/sample_questions.json --key tests/sample_key.json

## 运行盲测评分

    python scripts/score_blind.py --questions tests/sample_questions.json --key tests/sample_key.json --answers tests/sample_answers.json

## 拆分答案键

    python scripts/split_answer_key.py --input combined.json --questions-out questions.json --key-out key.json

## 新增能力

- GitHub 100 Skill 参考库
- 持久教练档案与决策日志
- 意图路由与输出模式

- 去标识化真实场景案例库（20 类）
- 小红书访问限制记录

- 普通成年人学术论文库
- Europe PMC 检索脚本与检索规范

- 社区高频问题地图与平台覆盖说明
- 基于问题分类和安全分诊的正确率提升协议

- 阿衡教练人设与输出边界
- 成人身体图像分析前置检查
- 静态可见肌肉、对称性和体态观察规范
- readiness 启发式评分
- sRPE 训练负荷与 volume load 计算
- 同类 Skill 能力对比

## 当前验证

- 1000 题题库结构校验通过
- 5 题最小回归样例评分通过
- 100 题回归测试正确率 91%

## 发布前检查

- 核实所有引用和版本
- 清除个人或客户数据
- 不包含未授权教材、课程、视频或题库
- 对疾病、孕期、进食障碍和特殊人群设置转介边界
- 用独立测试集验证题库质量
- 不将模拟分数等同于官方认证

## 免责声明

本 Skill 用于一般健康教育和训练规划，不构成医疗诊断、治疗或个体化临床营养处方。
