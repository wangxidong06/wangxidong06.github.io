# Xidong Wang — academic homepage

Personal website for **wangxidong06.github.io**, built with static HTML/CSS and a small Python Markdown generator. Includes About, Publications, Blog, a compiled PDF CV, and an Atom feed. No JavaScript is required to read the site.

## 本地构建和预览

```bash
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8000 --bind 127.0.0.1
```

打开 `http://localhost:8000`。如果运行在远端机器，请用编辑器的端口转发功能访问。

## 发布 Blog

1. 复制 `content/posts/_template.md`，命名为 `YYYY-MM-DD-your-topic.md`。
2. 修改头部的 `title`、`date`、`summary`、`tag`，正文使用 Markdown。
3. `status: draft` 不会发布；写好后改为 `status: published`。
4. 执行 `python scripts/build.py` 和 `python scripts/check.py` 检查效果。
5. 提交并 push 到 `main`，GitHub Actions 会构建并部署。

首页自动展示最近两篇文章，Blog 页按日期倒序排列，`blog/feed.xml` 可订阅。图片放在 `assets/`，文章中使用 `../../assets/文件名`。删除文章或改为草稿后，下一次构建会移除其公开页面。

## 修改个人信息

- `scripts/build.py`：个人介绍、经历、教育、教学和服务。
- `publications.json`：论文条目、作者、会议及论文/代码链接。
- `assets/style.css`：字体、颜色、间距、移动端和打印布局。
- `assets/portrait.png`：头像，使用本人提供的正式照片。
- `assets/Xidong_Wang_CV.pdf`：从 `../iResume/resume.tex` 编译的英文 CV，导航直接打开 PDF。

公开页面和 PDF 使用学术邮箱作为联系方式。LaTeX 源文件维护在独立的 iResume 仓库中。

## GitHub Pages

仓库名称必须是 `wangxidong06.github.io`。创建公开仓库后，将这些文件推送至 `main`，在 Settings → Pages → Build and deployment 中选择 **GitHub Actions**。`.github/workflows/pages.yml` 已配置自动部署，仅打包公开网页，不发布草稿和构建脚本。

登录后可以运行 `bash scripts/deploy.sh`，该脚本会验证 GitHub 账号、创建不存在的仓库、推送并启用 Pages。已有非空同名仓库会停止，避免覆盖现有网站。

## 内容和设计

论文清单共 20 篇，依据本人提供的 Scholar 列表更新。共同一作标记按本人资料保留，新增论文的完整作者信息参考 arXiv / ACL Anthology。ClinAlign 已替换旧版 From Rubrics to Principles 条目。期刊版 LLMs for Doctors 使用 2025 年，预印本为 2024 年；部分条目保留本人提供的常用标题。

`publications.json` 内的引用数是本人提供的快照，并非实时数据，逐篇引用数不在页面显示，页面保留原简历 2K+ 总引用里程碑。主页展示代表作，Publications 页面列出完整清单并支持方向筛选。Blog 当前留空，草稿模板保留。

设计参考 [Rongsheng Wang](https://w-r-s.github.io/) 和 [Junying Chen](https://jymchen.github.io/) 的紧凑学术排版与论文层次，保留独立 Blog 导航；实现为原创。

## Research profile and publication ordering

Research introduction emphasizes democratizing LLMs through efficient training, adaptation, architectures, and reinforcement learning. Earlier medical AI work is framed as AI for social good. `priority` in the publication data controls the six featured papers. IQuest-Q1 Technical Report currently links to the official blog, pending a report URL. Restored impact highlights (2K+ citations, 120K+/824K+ Hugging Face downloads, 2.9K+ GitHub stars) are previously reported milestones from the original CV, not live counters.

Publication order: the six requested featured papers come first; remaining papers retain their original source-list order (`display_order`). CMB includes its official website link. The 2K+ citation count was updated by the author.
