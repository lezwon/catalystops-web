# CatalystOps — Website

Marketing website for [CatalystOps](https://marketplace.visualstudio.com/items?itemName=CatalystOps.catalystops), a free VS Code extension that catches PySpark and Databricks performance issues before they hit production.

Live at **[catalystops.dev](https://catalystops.dev)**

## What is CatalystOps?

CatalystOps is a VS Code extension by [SpendOps](https://catalystops.dev) that brings Spark query analysis directly into your editor. Instead of context-switching to the Databricks UI, Spark History Server, or a billing console, everything surfaces inline as you write code.

**Key features:**

- **30+ anti-pattern detectors** — static analysis that runs locally with no cluster required. Catches `collect()`, cross joins, UDFs replacing built-ins, unsafe Delta writes, SQL injection via f-strings, schema drift, and more.
- **Dry-run plan analysis** — submits a neutralized version of your script to Databricks (cluster or Serverless), returns the physical Catalyst plan with sort-merge join detection, broadcast thresholds, and shuffle analysis.
- **Explain Plan tree & DAG** — interactive sidebar tree of the physical plan with per-node cost scores, plus a one-click DAG webview. Context-aware quick fixes on plan nodes: broadcast hints, repartition, persist, AQE config.
- **Billing dashboard** — queries `system.billing.usage` directly from VS Code, showing DBU and dollar spend broken down by user, workload type, and job. 1-hour cache, custom date ranges.
- **Schema validation** — tracks inferred schemas across DataFrames, validates join column types, detects silent `union()` column-order mismatches.
- **MCP server** — built-in Streamable HTTP MCP server auto-discovered by VS Code 1.99+. Claude, GitHub Copilot, Cursor, and Windsurf can call CatalystOps tools directly to analyze code, fetch billing data, and run dry runs through natural language.

**Free and Elastic License 2.0.** Available on the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=CatalystOps.catalystops) and [Open VSX](https://open-vsx.org/extension/CatalystOps/catalystops).

## Links

- Extension: [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=CatalystOps.catalystops)
- Extension source: [github.com/lezwon/CatalystOps](https://github.com/lezwon/CatalystOps)
- Open VSX: [open-vsx.org/extension/CatalystOps/catalystops](https://open-vsx.org/extension/CatalystOps/catalystops)
