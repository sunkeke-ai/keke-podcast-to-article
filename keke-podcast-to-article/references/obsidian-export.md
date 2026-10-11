# 通用Obsidian保存

Skill包只包含通用代码、说明与示例；绝不写入真实用户名、仓库绝对路径、文章、图片或个人配置。用户设置保存在本机 `~/.config/keke-podcast-to-article/config.json`；设置了XDG_CONFIG_HOME时跟随该目录。不同电脑分别设置，无需修改Skill。支持用 `--config` 指定独立配置文件，供多仓库使用。

## 首次设置

用户希望保存时，询问仓库根路径、文章子目录和附件子目录。只需要一次，后续读取本地配置。可建议 `Articles/Podcasts`、`Attachments/Podcasts`，但不能强迫用户改现有目录。检查仓库根有 `.obsidian`；多个仓库时由用户选择，不能自动猜当前仓库。

使用Skill目录中的脚本（路径按安装位置解析）：

```sh
python3 scripts/save_to_obsidian.py configure --vault '/path/to/your/vault' --articles-dir 'Articles/Podcasts' --assets-dir 'Attachments/Podcasts' --save-mode on_request
```

`on_request`：用户说“存入Obsidian”才保存。`auto_final`：用户明确设置此偏好后，最终成稿和已接受图片完成时自动保存；首图未确认或文章仍在修改阶段，工作文件保留在工作目录，不冒充最终成稿。设置成功不等于授权写入任何现有文章。

## 一次保存文章与配图

先把正文整理成真实Markdown文件，在各章节合适位置插入已有配图的绝对路径Markdown嵌入。保留来源链接、必要出处和已有元数据，不把编辑备注当正文。调用脚本，重复传入各张配图：

```sh
python3 scripts/save_to_obsidian.py save --article '/path/to/article.md' --title '文章标题' --asset '/path/to/section-01.png' --dry-run
python3 scripts/save_to_obsidian.py save --article '/path/to/article.md' --title '文章标题' --asset '/path/to/section-01.png'
```

先检查dry-run的目标路径，再在已有用户保存授权及环境写权限内执行。保存命令复制配图到仓库附件目录，改正文图链为相对路径，保证移动工作目录后仍可读。内容相同不重复保存；同名不同内容另存编号版本，不覆盖旧文。保存后返回实际文章路径，可打开文件帮助用户找到。

不默认修改日记。用户要“今日文章”入口时，读取其日记设置或明确的路径约定，按当天日期添加成稿链接，不重复追加。该功能由代理按需操作，脚本只负责文章和附件导出。原稿单独保存需用户明确要求。

## 可分发性与依赖

导出只用Python3标准库，不需要Obsidian API、账号或云服务，支持本地可写仓库；沙盒仍可能要求文件夹写权限。仓库未在当前电脑挂载时只提供工作目录文件，不宣称保存成功。

文章整理不依赖Punk；自动配图需要用户安装可用的punk-cover、对应风格资源和图像生成能力。缺少依赖时仍交付文章，并说明配图尚未完成。不要把个人风格资源或第三方Skill复制进公开仓库，除非已确认许可。
