# DoF · Embodied AI

**Embodied AI, understood. / 具身智能，从理解开始。**

DoF brings together **Paper Breakdown** and **Infra**: research explained through its original evidence, and the foundations that connect embodied AI systems. Watch videos, read bilingual companions, inspect original paper figures and explore interactive mechanisms. English is the default language; an explicit Chinese preference is preserved.

DoF 以 **Paper Breakdown · 论文解读** 和 **Infra · 认知基础** 两大分类组织内容。结合视频、双语伴读、原论文图和可操作实验，连接具体研究与具身智能基础。默认显示英文，并保留用户主动选择的中文偏好。

- **Website / 主页:** [dld0621.github.io/DoF](https://dld0621.github.io/DoF/)
- **Research map / 调研库:** [DoF Embodied AI Paper Analysis](https://github.com/Dld0621/Embodied-AI-Paper-Analysis)

## Paper Breakdown / 论文解读

Paper-led explanations connect the problem, method, baselines, experiments and limitations to the original paper and author demonstrations. Browse this collection from the [DoF library](https://dld0621.github.io/DoF/#library).

论文解读围绕具体论文，拆解问题、方法、baseline、实验与边界，并保留原论文图和作者演示的来源。

## Infra / 认知基础

Infra groups foundational explainers and deeper topic collections. **Dexterous Retargeting, VLA and World Models all belong to Infra**, with six chapters per topic.

Infra 汇集基础概念与专题深度解析。**灵巧手重定向、VLA 和世界模型均归入 Infra**，每个专题包含六章。

| Infra topic / 专题 | Chapters / 章节 | Method profiles / 方法档案 | Interactive experiments / 交互实验 |
| --- | ---: | ---: | ---: |
| [Dexterous Retargeting · 灵巧手重定向](https://dld0621.github.io/DoF/retargeting/) | 6 | 28 | 3 |
| [Vision–Language–Action Models · 视觉·语言·动作模型](https://dld0621.github.io/DoF/vla/) | 6 | 17 | 3 |
| [World Models · 世界模型](https://dld0621.github.io/DoF/world-models/) | 6 | 24 | 3 |

The full library contains **43 entries and 64 video variants**. The three Infra topics contribute **18 deep-dive chapters**. Method profiles include models, baselines, training methods and related approaches; profile counts are not a count of distinct model architectures.

完整内容库包含 **43 个条目、64 个视频版本**，其中三个 Infra 专题共 **18 个深度章节**。方法档案分别介绍模型、baseline、训练方法与相关路线；方法档案数量不等于独立模型架构数量。

### What you can explore / 可以学到什么

- **Retargeting:** coordinate frames, geometric objectives, learned mappings, contact, physical execution and fair evaluation. / 从坐标、几何目标和学习映射，走到接触、物理执行与公平评测。
- **VLA:** observations and instructions, action interfaces, model families, training data and execution timing. Experiments separate units and frames, quantization and chunks, and latency and queue behavior. / 拆开观测与指令、动作接口、模型家族、训练数据和执行时序；亲手区分单位与坐标、量化与动作块、延迟与队列。
- **World models:** hidden state, dynamics, imagination, planning, video models and connections to action. Experiments distinguish observation and process noise, execute CEM/MPC plans step by step, and examine rollout error and uncertainty. / 连接隐藏状态、动力学、想象、规划、视频模型与动作；区分两类噪声，逐步执行 CEM/MPC，并观察滚动误差与不确定性。

Original figures and selected author demonstrations retain source citations. Interactive numbers come from explicit teaching models; they do not represent new benchmark results or reproductions of the papers.

原论文图和作者演示保留来源。交互实验的数值来自明确的教学模型，不代表新增基准结果或原论文复现。

## Hosting / 托管方式

GitHub Pages serves the static site from the `main` branch, root directory. `.nojekyll` preserves the static files. No Node installation, application server, Worker or API key is needed to serve the frontend.

**Video files remain externally hosted** at `https://dof-embodied-ai.steven12123.chatgpt.site/media/`. They are not stored in this repository. GitHub Pages hosts the pages, scripts, figures and reading materials; video playback depends on the existing media service remaining available.

GitHub Pages 托管页面、脚本、原图与伴读资料。**视频继续使用现有外部媒体服务**，不把大型视频重复存入 Git 仓库；播放依赖该媒体服务持续可用。

## Updating the static export / 更新静态站点

Export a completed static source directory into a separate destination:

```sh
python3 scripts/build-pages.py --source ./source-public --output ./pages-output --repo-base /DoF/ --site-origin https://dld0621.github.io
```

Review the export manifest before replacing repository contents. Check the `/DoF/` project path, language switching, library search, chapter navigation, original-figure links and actual video playback. The exporter preserves image bytes, checks local targets and rejects detected private filesystem paths or credential patterns. It does not publish or push anything.

更新前核对导出清单、项目路径、中英切换、搜索、章节导航、原图来源与实际视频播放。导出命令本身不上传、不提交，也不发布。

## Attribution / 来源与署名

Paper figures, research findings, third-party demonstrations and linked media remain subject to their respective authors’ terms. Source links accompany the relevant chapters and method profiles. This repository does not grant a new license to third-party material or imply author endorsement.

Narration is AI-generated. Videos identify the music and research sources used. Training data, test conditions, model versions and evaluation protocols should be checked before comparing research results.

论文图、研究结论、第三方演示和链接媒体的权利仍归相应作者或权利人。视频使用 AI 合成讲解，并保留音乐与研究来源；比较结果时，应同时核对版本、数据、测试条件与评测协议。
