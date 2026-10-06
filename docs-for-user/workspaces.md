# 工作区与学习数据

工作区 = 独立的学习数据桶（资料、会话、进度、产物）。未选 = 默认工作区。

- 选工作区：普通对话在输入框选；书籍/掌握路径/阅读/观看在开始弹窗选。
- 侧栏历史汇总各工作区，打开即进入其工作区。
- 旧数据全归默认工作区。整理用「设置 → 个人 → 数据迁移」。

## 存放

- 默认：保留 `data/user/workspace/` 等历史路径。
- 自建：文件夹内 `.deeptutor/data/`；可看产物在 `outputs/`。
- 账号级（不隔离）：设置、凭据、工作区登记、记忆。

<details><summary>创建、切换、归档</summary>

设置 → 个人 → 工作区：创建/重命名/归档。切换重载页面、清缓存；已跑任务写旧区。链接带工作区，首页/设置不继承。未发送草稿暂存原区。
移动对话连附件产物一起走；运行中不可移。归档留数据、禁写入。

</details>

<details><summary>数据迁移/导出/换目录</summary>

设置 → 个人 → 数据迁移：选来源/目标/功能 → 预览 → 迁移。冲突（目标有数据/ID冲突）则拒，需建空区重试。保留快照、可恢复；记忆不迁；导出 ZIP 不含凭据。
工作区 → 迁移目录：只换位置，ID 不变。默认区完整搬家用数据迁移。

</details>

<details><summary>Partner、CLI/SDK、资源分配</summary>

- Partner：建时「资料库」绑工作区，共享文件/KB/技能，产物进该区 `outputs/`。默认私有区。归档/非所有者区不可绑。
- CLI：`deeptutor run chat "..." --workspace ws_...`，不填 = 默认。SDK：`DeepTutorApp(workspace_id="ws_...")`。HTTP：`?dt_workspace=` 或头 `X-DeepTutor-Workspace`。
- 资源：设置 → 工作区：继承全部 vs 仅所选（空 = 禁用该类）。改后下轮生效，不删历史。详情见 `workspace-resources-verification.md`（指针）。
- 管理员共享 KB 权限不变；个人进度按区分。实现审计见 `workspace-isolation-implementation.md`（指针）。观看见 `watching-workspace.md`（指针）。

</details>
