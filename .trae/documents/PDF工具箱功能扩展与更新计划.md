## 项目概览
- 类型：Python + Tkinter 桌面应用，聚焦 PDF 合并/分割/转换/安全
- 入口：`main.py`（GUI）与 `run.py`（诊断）
- GUI：`src/gui/main_window.py` 四个页签（合并/分割/转换/安全），所有耗时任务线程化
- 模块：
  - 合并：`src/pdf_merger.py`（`merge_pdfs` 与 `merge_pdfs_with_order`；信息查询）
  - 分割：`src/pdf_splitter.py`（按页数/范围、页面提取、页数查询）
  - 转换：`src/pdf_converter.py`（PDF→图片/文本、图片→PDF、压缩、信息查询）
  - 安全：`src/pdf_security.py`（加密/解密/去密码、加密信息查询）
- 打包：`build_exe.py`、`build_console.py`、`build_test.py`
- 依赖：`requirements.txt`（PyPDF2、PyMuPDF、Pillow、img2pdf、reportlab、tkinter-tooltip）

## 现有功能总结
- PDF合并：选择多文件→输出一个 PDF（`src/gui/main_window.py:470-495` 调用 `PDFMerger.merge_pdfs`）
- PDF分割：两模式（每 N 页/页码范围），输出到目录（`src/gui/main_window.py:506-541`）
- 格式转换：PDF→图片/文本、图片→PDF、PDF压缩（`src/gui/main_window.py:558-607`）
- 安全：加密/解密/移除密码（`src/gui/main_window.py:618-655`）
- 日志：统一记录到 UI 与文件（`main.py:24-33`、`src/gui/main_window.py:658-666`）

## 目标与原则
- 不增加重量级外部依赖（保持打包友好与跨平台）
- 复用现有模块化结构与库（PyPDF2、PyMuPDF、Pillow、img2pdf）
- 明确的 UI 操作路径、可见的进度与可取消
- 代码风格与结构保持一致（面向对象、线程任务、错误与日志统一）

## 扩展功能方案
1. 合并页签增强
- 文件排序：为列表提供“上移/下移/置顶/置底”按钮，反映到 `self.merge_file_list`
- 页范围合并：在每个文件项旁支持输入页码范围，调用 `PDFMerger.merge_pdfs_with_order` 替代简单合并（`src/pdf_merger.py:45-81`）
- 预览：选中文件时显示第一页缩略图，便于确认文件顺序

2. 分割页签增强
- 新增“按书签分割”：基于 `PyMuPDF` 读取大纲，按顶层书签切分（适合目录分章）
- 新增“按文件大小分割”：根据目标体积近似切段（页粒度），用于邮件或上传限制
- 预览范围校验：输入范围时显示有效页数与将生成的文件数

3. 转换页签增强
- 新增“提取图片”：从 PDF 中导出内嵌图像到目录（`fitz.Page.get_images()` + `doc.extract_image`）
- 暴露参数：PDF→图片支持选择 `format`、`dpi`；压缩支持垃圾回收等级与 `deflate` 选项
- PDF→文本：增加“仅纯文本/包含页号/导出 Markdown”选项（先提供文本格式开关）

4. 安全页签增强
- 权限控制：加密时设置权限（禁止打印/复制/修改等），映射到 `PyPDF2.PdfWriter.encrypt(..., permissions=...)`
- 查看当前加密信息：在 UI 直接展示 `get_encryption_info` 返回（`src/pdf_security.py:122-155`）

5. 通用体验与稳定性
- 拖拽添加文件：在主文件列表与合并列表支持拖拽
- 进度条与取消：为所有线程化任务增加进度指示与取消开关（线程间共享标志）
- 最近输出路径：记忆每个页签最近选择的目录/文件（简单配置保存到本地）
- 工具提示：为关键控件添加 `tkinter-tooltip` 提示文案

6. 高级工具（可选）
- 水印/页眉页脚：新增页签，支持文字/图片水印、页码页眉页脚（基于 `fitz` 叠加绘制）
- 页面编辑：旋转、裁剪、重新排序（轻量交互，作用于合并前列表）

## 技术实现细则
- GUI改动（`src/gui/main_window.py`）
  - 合并：
    - 增加排序按钮与事件，操作 `self.merge_file_list` 与 `self.merge_file_listbox`
    - 每项页范围：为列表项维护字典 `{path: range_str}`，合并时转换为 `[(path, range_str)]`
    - 预览区域：右侧 `ttk.Label` 显示由 `PDFConverter.pdf_to_images(..., page_range=[1])` 生成的缩略图路径
  - 分割：
    - 单选新增“按书签/按大小”，分别触发新方法 `split_by_bookmarks` 与 `split_by_size`
    - 在操作前显示总页数与预计输出数量
  - 转换：
    - 新增“提取图片”到转换类型下拉；参数控件（format、dpi）
  - 安全：
    - 权限复选框（打印、复制、注释、表单填充等），组合成权限掩码传入 `encrypt_pdf`
  - 通用：
    - 统一进度条 `ttk.Progressbar` 与“取消”按钮；线程检查 `self.cancel_flag`
    - 记忆输出路径：使用简单的 `json` 配置读写（启动加载、关闭保存）
- 模块扩展
  - `src/pdf_merger.py`：暴露页范围合并已具备；新增校验与错误提示路径
  - `src/pdf_splitter.py`：
    - `split_by_bookmarks(input_file, output_dir, level=1)`：读取 `doc.get_toc()`，按给定层级分块写出
    - `split_by_size(input_file, output_dir, target_mb)`：估算页大小，分页聚合直至接近目标大小
  - `src/pdf_converter.py`：
    - `extract_images(input_file, output_dir)`：遍历页与 `get_images()`，导出 PNG/JPEG 原始图
    - `pdf_to_images(...)`：参数透传与格式校验
  - `src/pdf_security.py`：
    - `encrypt_pdf(..., permissions)`：结合 `PyPDF2` 权限枚举构建权限集合
- 依赖与打包
  - 继续使用现有依赖；不引入 OCR 等重量库
  - 打包脚本：如新增资源（图标/本地化文件）再扩展 `--add-data`

## 验证与测试
- 功能自测用例：
  - 合并（含页范围与排序）：多文件、多范围、存在无效页范围的错误提示
  - 分割（页数/范围/书签/大小）：不同页数与边界；输出文件命名与数量检查
  - 转换（PDF→图片/文本/压缩/提取图片）：参数生效与输出格式正确
  - 安全（加密/解密/去密码/权限）：不同密码与权限组合，结果可打开且权限生效
- 打包验证：构建 `windowed` 与 `console` 版本，运行最小测试 `test_simple.py`
- 日志检查：关键路径与错误均有清晰日志

## 拟定更新日志 v1.1.0
- 新增：PDF合并支持文件排序与按文件页范围合并（含预览）
- 新增：分割支持按书签与按目标大小拆分
- 新增：转换支持“提取图片”，并暴露 PDF→图片的格式与 DPI 选项
- 新增：加密权限控制与加密信息查看
- 改进：所有长任务新增进度条与取消操作；记忆各功能页的最近输出路径
- 改进：为主要控件增加工具提示，提升可用性
- 修复/优化：统一错误提示与输入校验；压缩参数可调

## 风险与兼容性
- PyPDF2 权限 API 在不同版本存在差异，需按 `3.x` 验证；若不稳定则仅在 UI 显示提示并退化到基础加密
- 书签拆分依赖 PDF 大纲的质量；对无大纲或嵌套复杂文档需提供兜底策略（退化为页范围拆分）
- 目标大小拆分为近似策略，边界情况会偏差；在 UI 说明“近似值”

## 下一步
- 按上述方案更新 GUI 与模块，保持现有结构与风格
- 交付后提供一套典型样例与简单脚本，便于复现与验证