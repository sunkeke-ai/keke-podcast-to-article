# 可可的播客对谈精华改稿

把 YouTube、小宇宙单集链接或逐字稿整理成中文精华长文，先生成第一章节完整内容配图，确认后逐章配图，支持一条指令保存到自己的 Obsidian。
![Uploading readme-workflow.png…]()

## 默认工作流

1. 获取可靠文字稿并通读，按读者关心的问题重组文章。
2. 保留关键原声，区分直接引用、整理引用和作者提炼。
3. 根据第一正文章节的完整内容生成配图，默认 3:2、极简视觉隐喻风。
4. 展示文章与首图，等用户确认；确认后为其余正文章节各生成一张。
5. 用户说“存入 Obsidian”时，将成稿与配图一起导出到本机配置的仓库。

配图支持自选章节、一次全部生成、仅提示词或不配图。文章章节数量随内容变化。

## 安装与调用

在 Codex 中，将仓库内容放入 `~/.codex/skills/keke-podcast-to-article/`。使用其他支持 Skill 的代理时，将本目录放到该代理的 Skill 目录。必要时重新打开会话以加载技能。

```sh
git clone https://github.com/sunkeke-ai/keke-podcast-to-article.git ~/.codex/skills/keke-podcast-to-article
```

如果目标目录已存在，先备份或更新现有安装，不要覆盖个人改动。

调用示例：

```text
用 $keke-podcast-to-article 处理这个链接：[YouTube 或小宇宙链接]
用 $keke-podcast-to-article 整理这份逐字稿，只要文章，暂不配图。
第一张效果可以，继续为其余章节配图。
把这篇成稿和已确认的配图存入 Obsidian。
```

## 能力与依赖

- **文章整理**：由运行此 Skill 的代理完成，不需要额外 Python 库。
- **链接输入**：需要可用的浏览、字幕获取或音频转写能力。并非所有链接都能获取完整内容；遇到限制会请用户提供原稿，不凭简介编造访谈。
- **Punk 配图**：需要另行安装 `punk-cover`、对应风格资源以及可用图像生成能力。本仓库不附带这些第三方依赖。缺少时仍可整理文章，配图能力在安装依赖后可用。
- **Obsidian 导出**：需要 Python 3.9+ 和本机可写的 Obsidian 仓库，只用标准库，无需 Obsidian API、账号或云服务。中文文件按 UTF-8 保存。

## 配置自己的 Obsidian

告诉代理：“配置 Obsidian 保存，仓库是……，文章放……，附件放……”。首次配置后无需每次重复路径。

也可以在本仓库目录执行：

```sh
python3 scripts/save_to_obsidian.py configure --vault '/path/to/your/vault' --articles-dir 'Articles/Podcasts' --assets-dir 'Attachments/Podcasts' --save-mode on_request
```

Windows 路径也可作为 `--vault` 的参数，目录参数使用自己仓库内的相对路径。

配置保存在本机 `~/.config/keke-podcast-to-article/config.json`（遵循 `XDG_CONFIG_HOME`），不放进公开仓库。`--config` 可指定不同配置以支持多个仓库。

- `on_request`：说“存入 Obsidian”才保存，默认使用此模式。
- `auto_final`：用户明确启用后，最终成稿与已接受图片完成时自动保存，不跳过首图确认。

脚本复制图片并更新正文图链，相同内容重复保存不生成副本，同名修改另存编号版本。默认不更改日记，也不归档原稿；这些可按用户需求扩展。

完整命令见 [Obsidian 保存说明](references/obsidian-export.md)。

## 文件结构

```text
SKILL.md                        核心写作与配图规则
agents/openai.yaml              Codex 展示信息
references/editorial-examples.md 编辑实例
references/source-input-workflow.md 链接输入流程
references/punk-illustration-workflow.md 内容配图流程
references/obsidian-export.md   通用导出说明
scripts/save_to_obsidian.py     本机配置与文章附件导出
```

## 公开与私人设置

本仓库只包含规则、代码与通用示例，不包含作者的个人配置、真实仓库路径、访谈原稿、成稿或生成图片。不要把本机配置文件提交到 GitHub。

本仓库使用 [MIT License](LICENSE)。第三方 Skill、风格资源与平台内容各自遵循其许可，不在本仓库授权范围内。
