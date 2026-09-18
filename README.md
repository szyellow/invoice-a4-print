# 发票 A4 合并打印

一个用于 Codex 的 Skill：将 PDF 发票排成竖向 A4，每页上下两张，生成可直接打印的 PDF。

## 功能

- 按指定文件顺序合并，支持多页 PDF。
- 奇数张时，最后一张放在新页上半部。
- 等比缩放，保留原始 PDF 文字与图形，不将发票转换为截图。
- 只处理当前指定批次，不修改源文件。
- 生成后检查页面尺寸与视觉排版。

## 安装与调用

将此仓库文件放入个人技能目录的 `invoice-a4-print` 文件夹。默认个人技能目录为 `~/.codex/skills`；如果设置了 `CODEX_HOME`，则使用其下的 `skills` 目录。

上传 PDF 后输入：

> 使用 $invoice-a4-print，把这些发票合并成每张 A4 两张的打印版。

## 独立运行

需要 Python 3 和 pypdf：

```bash
python -m pip install -r requirements.txt
python scripts/combine_invoices.py --output merged-a4.pdf invoice-1.pdf invoice-2.pdf
```

输出文件名必须尚未存在。密码保护的 PDF 需要先提供可读取副本。

脚本按每个源页面一张发票处理。源页已有多张发票或大量空白时，需要先检查并调整内容区域。合并后可用 Poppler 的 `pdftoppm` 渲染检查。

## 打印设置

选择 **A4、纵向、实际大小（100%）、每张纸 1 页**。文件已经完成二合一排版，不要再次选择每张纸 2 页。

仓库仅包含技能说明与脚本，不包含实际发票。
