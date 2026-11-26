# RAWGraphs 参考源码索引

本页对照[参考库统计图形分析](https://github.com/fengbaifan/Infographic-Style-Repository/blob/111a6b42c7f6da436a5ad1ab82b9a40557f365dc/04-统计图形分析/README.md)，按 App、Charts 与 Core 三层列出固定版本的源码入口。适用于复核统计图的字段要求和计算。

## 从数据到图形

| 层 | 源码 | 核验内容 |
|---|---|---|
| App | [charts.js](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/src/charts.js) | 注册应用可选的图形。 |
| App | [worker.js](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/src/worker/worker.js) | 调用 Core 解析输入，并为所选图形传入数据、类型、字段映射与视觉选项。 |
| App | [package-lock.json](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/package-lock.json) | 核对依赖。此快照锁定 Charts 1.1.0、Core 1.0.0。 |
| Core | [dataset.js](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/src/dataset.js) | 先看 inferTypes，再看 parseDataset。核对类型推断和逐行解析。 |
| Core | [mapping.js](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/src/mapping.js) | 检查 validateMapping、annotateMapping 和 makeMapper，追踪字段验证、注解、取值和分组。 |
| Core | [expressionRegister.js](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/src/expressionRegister.js) | 核对 count、countDistinct、sum、mean、median 等聚合器。 |
| Core | [groupBy.js](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/src/groupBy.js) | 查看基于 Map 的分组辅助实现。 |
| Core | [rawGraphs.js](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/src/rawGraphs.js) | 定位图表配置和数据映射调用链。 |
| Core | [mapper.test.js](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/src/__tests__/mapper.test.js) | 查看合法和非法字段映射及输出示例。 |

## 各图形源码

先读字段声明，再看映射及渲染。映射允许一个图形使用多列，基础表仍保持一列一个字段。

| 图形 | 字段声明 | 数据映射 | 渲染 | 重点 |
|---|---|---|---|---|
| 条形图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchart/render.js) | 类别与系列分组，核查计行和汇总数量的区别。 |
| 堆叠条形图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchartstacked/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchartstacked/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchartstacked/render.js) | 子类同单位且可加，核查堆叠前的聚合。 |
| 折线图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/linechart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/linechart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/linechart/render.js) | 同系列内的横轴顺序、重复横坐标及缺测。 |
| 甘特图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/ganttChart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/ganttChart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/ganttChart/render.js) | 起止时间各占一列，长度对应时间跨度。 |
| 矩阵图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/matrixplot/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/matrixplot/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/matrixplot/render.js) | 按两维度的交叉组合计算，区分零、空白及缺数据。 |
| 旭日图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sunburst/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sunburst/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sunburst/render.js) | 层级路径与权重，检查重复叶节点是否重复计量。 |
| 桑基图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sankeydiagram/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sankeydiagram/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sankeydiagram/render.js) | 来源、目标及流量，检查连线宽度的分母和单位。 |
| 气泡图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bubblechart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bubblechart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bubblechart/render.js) | 核查坐标映射和数值到半径的尺度。 |
| 饼图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/piechart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/piechart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/piechart/render.js) | Arcs 接数值列，Series 可用于比较组。份额的分母来自同一组。 |
| 矩形树图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/treemap/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/treemap/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/treemap/render.js) | Hierarchy 接层级，Size 接度量。检查同单位、同口径的权重。 |
| 箱线图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/boxplot/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/boxplot/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/boxplot/render.js) | Y Axis 接单笔数值，Groups 可用于分组，渲染阶段求四分位数。 |
| 坡度图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/slopechart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/slopechart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/slopechart/render.js) | Source、Target 接配对的两个端点，Label 对应对象。两端保留同单位。 |
| 排名变化图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bumpchart/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bumpchart/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bumpchart/render.js) | X Axis、Streams 和 Ranking 用于按期追踪类别及名次，Size 可记录量级。 |
| 冲积图 | [字段](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/alluvialdiagram/dimensions.js) | [映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/alluvialdiagram/mapping.js) | [渲染](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/alluvialdiagram/render.js) | Steps 按阶段顺序映射类别字段，Size 可接满足可加条件的量值。 |

## 源码与案例之间如何互查

1. 确认案例每行代表的对象和度量，识别空值、零、重复记录与分母。
2. 用字段声明核对必填字段和类型。根据地图、时间或类别关系确定分组键。
3. 检查映射是否计算了行数、去重数、和或均值。用几行人工可复算的数据核对。
4. 检查渲染中位置、长度、面积、色彩和顺序的对应关系。记录与原图读法的差异。

[字段映射说明](01-RAWGraphs图形与字段映射.md) · [Terra 案例对照](02-Terra案例的数据结构与统计图形.md)

App、Charts 和 Core 的这三个快照均附 Apache License 2.0。[App 许可证](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/LICENSE) · [Charts 许可证](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/LICENSE) · [Core 许可证](https://github.com/rawgraphs/rawgraphs-core/blob/715cc49e2c98f2171aa818f5600817db9a4b3cd6/LICENSE)
