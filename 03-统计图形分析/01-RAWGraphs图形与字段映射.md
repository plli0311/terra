# RAWGraphs 图形与字段映射

RAWGraphs 的应用层先解析数据，再用图表声明的维度接收字段。维度声明可规定允许的字段类型、是否必填、是否允许多字段以及是否支持聚合。工作线程将数据、数据类型、映射和视觉选项交给核心库。分析案例时可以沿相同路径反推：先确认一行代表什么，再确认哪些字段参加分组或计算，最后判断图形通道如何表达结果。

- [应用图表注册表](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/src/charts.js)
- [字段映射界面](https://github.com/rawgraphs/rawgraphs-app/tree/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/src/components/DataMapping)
- [解析与映射工作线程](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/src/worker/worker.js)
- [应用依赖锁定文件](https://github.com/rawgraphs/rawgraphs-app/blob/48c3b2ee9ff412721a2c99c7bed38e734b3fa534/package-lock.json)

应用锁定 Charts 1.1.0 和 Core 1.0.0。下表的实现细节来自独立 Charts 仓库的固定源码快照，用于解释图形原理。案例中的映射属于分析或重绘建议，实际制图软件与原始数据另行核实。

| 图形 | 一行代表什么及如何映射 | 计算与阅读判断 |
|---|---|---|
| 条形图 | 一条类别记录。Bars 接类别，Size 可接数值，Series 可分组。 | 源码按 Series 和 Bars 分组。Size 未映射时计行数，已映射时使用维度配置的聚合器。汇总表应使用已有数量列，先确认每组是否可求和。 |
| 堆叠条形图 | 一个分类下的一项子类值。X Axis 接分类，Size 接度量，Series 可接子类。 | 先按分组聚合，再堆叠。子类应有可比单位并可相加。展示百分比前应明确各组分母与标准化方式。 |
| 折线图 | 某时点或数值位置上的一次观测。X Axis 接日期或数值，Y Axis 接度量，Lines 可接系列。 | 需判断相同系列和横坐标内的多条记录如何汇总。连接线暗示有序变化。事件年表应保留同年多条记录。 |
| 甘特图 | 一个起止区间。Start date、End Date 必填，Groups 和 Color 可接字符串。 | 端点映射到时间位置，长度表示持续期。只有发生日期的事件应以点标注，起止未知的记录可保留为待核实。 |
| 矩阵图 | 一条行列组合记录。X Axis、Y Axis 接两个维度，Size、Color 和 Label 可选。 | 源码对交叉组聚合，Size 未映射时计行。排期只表达有无时，可维持同样大小的标记，并明确空白是无场次还是缺数据。 |
| 旭日图 | 一条从父级到叶节点的分类路径。Hierarchy 接有顺序的层级列，Size 可接数值。 | 使用层级分区定位弧段。若解释角宽为占比，需要明确权重与分母，并核查叶节点是否重复计入。 |
| 桑基图 | 一条源节点到目标节点的关系。Source node 和 Target node 必填，Size 可接流量。 | 先明确连线宽度表示什么，以及相同来源与去向如何汇总。步骤编号仅支持顺序推断，宽度需要独立流量依据。 |
| 气泡图 | 一条具备两个坐标字段的观测。X、Y 接数值或日期，Size 可接第三个数值。 | 源码使用平方根尺度计算圆半径。读面积前核查域、半径范围与图例。尺寸、透明度和重叠都可能改变视觉印象。 |

[条形图映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchart/mapping.js) · [堆叠条形图](https://github.com/rawgraphs/rawgraphs-charts/tree/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/barchartstacked) · [折线图](https://github.com/rawgraphs/rawgraphs-charts/tree/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/linechart) · [甘特图](https://github.com/rawgraphs/rawgraphs-charts/tree/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/ganttChart) · [矩阵映射](https://github.com/rawgraphs/rawgraphs-charts/blob/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/matrixplot/mapping.js) · [旭日图](https://github.com/rawgraphs/rawgraphs-charts/tree/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sunburst) · [桑基图](https://github.com/rawgraphs/rawgraphs-charts/tree/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/sankeydiagram) · [气泡图](https://github.com/rawgraphs/rawgraphs-charts/tree/cade3b6e1b4d35d365440b1365d51b0dd48c9bce/src/bubblechart)
