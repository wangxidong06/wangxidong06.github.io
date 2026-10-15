# Xidong Wang — academic homepage

Personal website for **wangxidong06.github.io**, built with static HTML/CSS and a small Python Markdown generator. Includes About, Publications, Blog, a printable CV, and an Atom feed. No JavaScript is required to read the site.

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
- `assets/portrait.png`：头像，初版来自本人 GitHub 公开头像。
- CV 页面可使用浏览器打印功能保存 PDF。

原始简历中的电话号码没有放入公开页面，原始 LaTeX 文件不随网站发布。

## GitHub Pages

仓库名称必须是 `wangxidong06.github.io`。创建公开仓库后，将这些文件推送至 `main`，在 Settings → Pages → Build and deployment 中选择 **GitHub Actions**。`.github/workflows/pages.yml` 已配置自动部署，仅打包公开网页，不发布草稿和构建脚本。

登录后可以运行 `bash scripts/deploy.sh`，该脚本会验证 GitHub 账号、创建不存在的仓库、推送并启用 Pages。已有非空同名仓库会停止，避免覆盖现有网站。

## 内容来源与待确认项

初始资料来自 `../myresume/resume.tex`。CMB、Huatuo-26M 作者列表依据 ACL Anthology 的正式发表记录修正。LiveClin 博文仅总结原论文实验，不代表实时榜单。

简历中的 “From Rubrics to Principles” 与检索到的 ClinAlign 标题不同，初版保留简历的标题和作者，暂不添加可能指向不同版本的论文链接。Scholar 当时限流，因此未写入引用数；下载量和 star 数也没有作为实时数据展示。

设计参考 [Yue Ma](https://mayuelala.github.io/) 的学术内容结构和 [Tianyu Gao](https://gaotianyu.xyz/about/) 的简洁排版；页面实现为原创。
