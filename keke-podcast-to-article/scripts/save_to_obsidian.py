#!/usr/bin/env python3
"""Portable local Obsidian export. Uses only Python's standard library."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote


def config_path():
    base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
    return base / 'keke-podcast-to-article' / 'config.json'


def inside(vault, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('保存目录必须是仓库内的相对路径')
    target = (vault / rel).resolve()
    if not target.is_relative_to(vault):
        raise ValueError('保存路径不能越出仓库（包括符号链接）')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=config_path())
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('configure')
    init.add_argument('--vault', required=True, type=Path)
    init.add_argument('--articles-dir', default='Articles/Podcasts')
    init.add_argument('--assets-dir', default='Attachments/Podcasts')
    init.add_argument('--save-mode', choices=['on_request', 'auto_final'], default='on_request')
    save = sub.add_parser('save')
    save.add_argument('--article', required=True, type=Path)
    save.add_argument('--title', required=True)
    save.add_argument('--asset', action='append', default=[], type=Path,
                      help='Image referenced by its absolute path in article; repeat for each image')
    save.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.command == 'configure':
        vault = args.vault.expanduser().resolve()
        if not vault.is_dir() or not (vault / '.obsidian').is_dir():
            raise ValueError('请指定已存在的Obsidian仓库根目录（包含.obsidian）')
        inside(vault, args.articles_dir)
        inside(vault, args.assets_dir)
        data = {'version': 1, 'vault_path': str(vault),
                'articles_dir': args.articles_dir, 'assets_dir': args.assets_dir,
                'save_mode': args.save_mode}
        args.config.parent.mkdir(parents=True, exist_ok=True)
        args.config.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'configured': str(args.config)}, ensure_ascii=False))
        return
    data = json.loads(args.config.read_text(encoding='utf-8'))
    vault = Path(data['vault_path']).expanduser().resolve()
    if not vault.is_dir() or not (vault / '.obsidian').is_dir():
        raise ValueError('配置的仓库不可用，请重新配置')
    article_dir = inside(vault, data['articles_dir'])
    asset_dir = inside(vault, data['assets_dir'])
    title = re.sub(r'[\x00-\x1f<>:"/\\|?*\[\]#^]', '-', args.title).strip(' .')[:150]
    if not title:
        raise ValueError('文章标题不能为空')
    # Prepare and validate everything before writing.
    text = args.article.expanduser().read_text(encoding='utf-8')
    copies = []
    for supplied in args.asset:
        source = supplied.expanduser().resolve()
        if not source.is_file() or source.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
            raise ValueError('配图必须是已存在的图片文件')
        if str(source) not in text and str(supplied) not in text:
            raise ValueError('配图未在文章中以绝对路径引用：' + source.name)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        target = inside(vault, str(Path(data['assets_dir']) / (digest + source.suffix.lower())))
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError('已有附件内容不匹配')
        relative = os.path.relpath(target, article_dir).replace(os.sep, '/')
        text = text.replace(str(source), quote(relative, safe='/')).replace(str(supplied), quote(relative, safe='/'))
        copies.append((source, target))
    target = inside(vault, str(Path(data['articles_dir']) / (title + '.md')))
    number = 2
    while target.exists() and target.read_text(encoding='utf-8') != text:
        target = inside(vault, str(Path(data['articles_dir']) / (title + f'（{number}）.md')))
        number += 1
    result = {'article': str(target), 'assets': [str(p) for _, p in copies],
              'dry_run': args.dry_run}
    if not args.dry_run:
        article_dir.mkdir(parents=True, exist_ok=True)
        if copies:
            asset_dir.mkdir(parents=True, exist_ok=True)
        for source, dest in copies:
            if not dest.exists():
                shutil.copy2(source, dest)
        if not target.exists():
            with target.open('x', encoding='utf-8') as handle:
                handle.write(text)
        assert target.read_text(encoding='utf-8') == text
        assert all(dest.is_file() for _, dest in copies)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
