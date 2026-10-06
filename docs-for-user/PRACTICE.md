# 练习：题库、错题与每日复习

「学习空间 → 题库」（`/space/questions`）与「个性化学习 → 练习」（`/learning/practice`）共用题目与复习记录；前者无统计图和每日面板。

## 日常使用

- 题库 = 全部题；错题 = 答错过 + 手动导入。标签独立，多标签可共存。
- 流程：作答 → 看答案解析 → 反馈回忆情况。单选/多选/判断服务端判分；填空/简答自评。
- 新错自动入错题；复习答对仍保留；「已掌握」暂停安排，取消恢复；再错重启。

## 导入

支持 `.xlsx/.csv/.tsv/.json`，上限 **500 题、5 MB、64 列**。Excel 取活动工作表；CSV/TSV 用 UTF-8（含 BOM）或 GB18030；公式先粘贴为值。`.xls` 另存为 `.xlsx`。

| 列 | 内容 |
|---|---|
| `question`（题目） | 必填 |
| `question_type`（题型） | `single_choice/multi_choice/true_false/fill_blank/short_answer` 或中文名 |
| `A`…`J` | 选项，至少两个 |
| `correct_answer`（答案） | 必填：单选 `A`，多选 `A,C`，判断 `true/false`/对/错 |
| `explanation/tags/difficulty/user_answer` | 解析/标签（逗号或分号）/难度/历史作答，可选 |

JSON 为对象数组，选项可用 `options` 对象/数组。选「题库」或「错题」导入；有任一行非法则不开放确认；预览 24h 有效；重复题（同题干+题型+选项+答案）合并标签。

<details>
<summary>统计、复习算法、兼容</summary>

- 统计（7/30/90 天）：新增题目（入库日）、新增错题（首次变错题日）、复习次数（成功提交数）。按浏览器时区；选择存 URL。
- 每日复习：新错次日开始；逾期 + 今日到期组成队列，先到先练，每轮 20 题。Again≈1天；Hard≈×1.2；Good≈3天起延；Easy更长。上限365天。客观题答错只能 Again。SM-2 风格冷启动，非 FSRS。
- 兼容：旧写入接口继续用；新表 `practice_review_state/_events/imports`；删题清复习记录；回退前备份 DB。
</details>
