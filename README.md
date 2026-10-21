# Shadow3DAssetLibrary

原创柔和卡通低多边形 3D 素材库的第一资产卷，收录冻结为 **622 件**。现行浏览网页与未来新增资产已分开维护：

- [统一素材网页](https://shadow-xjy-games.github.io/Shadow3DAssetGallery/)：搜索、筛选、分页、滚动浏览与素材详情。
- [Shadow3DAssetGallery 网页仓库](https://github.com/shAdow-XJY-Games/Shadow3DAssetGallery)：网页代码、统一目录入口及后续目录更新。
- [Shadow3DAssetLibrary02 第二资产卷](https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary02)：未来新增资产的存放仓库。

## 第一卷保留内容

本卷的 622 件资产冻结于提交 `3bd5e2f0cb73b1810eaa483a3f42b7721921d094`。既有 `assets/` 路径、资产文件、版本、来源 ID、固定提交与 SHA-256 保持原值；完整 Git 历史继续保留。本次网页退役仅更新说明并移除已迁走的网页实现和相关网页构建、发布适配及测试工具，不修改任何资产、目录 JSON 或 schema。

保留内容包括：

- `assets/`：模型、Blender 源文件、生成脚本、渲染图与资产元数据。
- `catalog/`：内容寻址目录图及其历史节点。
- `docs/catalog.json`、`docs/catalog-v2.json`、`docs/catalog-v3.json`、`docs/metadata/`：冻结的目录入口与历史元数据。
- `schemas/`：原有资产与目录契约。

网页迁移初期，统一目录仍通过本卷固定元数据提交 `6fd0e581c17b06454c809c95e7b7f9e1d4971b90` 读取原有 622 件记录。关闭本卷 GitHub Pages 不会替代或更改这些固定提交引用；请使用上方的新素材网页作为浏览入口。

后续统一目录更新属于 Shadow3DAssetGallery，新资产属于 Shadow3DAssetLibrary02；不要继续向第一卷追加资产，或用第二卷的局部目录替换全局目录。网页开发与当前发布说明请查阅网页仓 README。保留的历史 schema 说明中涉及旧 `docs/` 网页模块或 `gallery/` 工具的段落属于当时的实现记录，不再作为本卷现行运行命令。

## Rights

All original project source, models and artwork: All rights reserved. Public visibility and download access are not an open-source or asset reuse license. Obtain separate permission before reuse.
