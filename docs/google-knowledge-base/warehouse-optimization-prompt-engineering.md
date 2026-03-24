Warehouse Optimization Prompt Engineering

Purpose  
This document defines a set of optimized prompts to help build, evaluate, and iterate on the Warehouse Optimization system. These prompts are intended for product design, architecture, data modeling, WMS integration, telemetry analysis, optimization logic, analytics, and implementation planning.

Guiding Principles for Prompts  
\- Be explicit about the output format.  
\- Ask for assumptions and uncertainties separately from conclusions.  
\- Prefer structured outputs over vague brainstorming.  
\- Ask for practical MVP-first recommendations before advanced solutions.  
\- Avoid jumping to reinforcement learning before validating simpler optimization methods.  
\- When working with warehouse data, separate raw observations, inferred patterns, and recommendations.  
\- When designing integrations, keep outputs vendor-neutral unless the task is specifically about ERPNext.

1\. Product Framing Prompts

Prompt: Product definition  
You are helping design a warehouse optimization product.

Context:  
\- The system combines warehouse telemetry, WMS data, and sales/order demand.  
\- The first WMS target is ERPNext.  
\- The system should eventually recommend route and layout improvements over time.  
\- Forklift telemetry includes 1 Hz position/orientation CSVs and state/beacon CSVs.

Task:  
Create a concise but serious product definition that includes:  
1\. problem statement  
2\. target users  
3\. core workflows  
4\. data inputs  
5\. outputs/recommendations  
6\. MVP scope  
7\. non-goals

Output format:  
Use numbered sections with clear headings.

Prompt: Value proposition refinement  
Given the current warehouse optimization concept, produce three versions of the value proposition:  
1\. investor-facing  
2\. client-facing  
3\. operations-manager-facing

Keep each version under 120 words and make each one meaningfully different.

2\. Technical Architecture Prompts

Prompt: MVP architecture decision prompt  
You are designing the MVP architecture for a warehouse optimization system.

Requirements:  
\- Python-first implementation  
\- ERPNext as the first WMS integration target  
\- CSV telemetry ingestion  
\- Power BI as reporting/output layer  
\- heuristics-first optimization, not RL-first  
\- future support for multiple WMS integrations

Task:  
Propose an MVP architecture with:  
1\. major components  
2\. data flow  
3\. interfaces between components  
4\. what should be synchronous vs asynchronous  
5\. what to defer until later

Output constraints:  
\- prioritize implementation realism  
\- avoid overengineering  
\- do not default to microservices unless justified

Prompt: Build-vs-buy architecture prompt  
Evaluate which parts of the system should be built from scratch versus delegated to existing systems.

Must cover:  
\- ERP/WMS responsibilities  
\- telemetry ingestion responsibilities  
\- optimization engine responsibilities  
\- reporting/dashboard responsibilities  
\- recommendation storage responsibilities

Output format:  
A table with columns: Capability, Build, Buy/Reuse, Recommendation, Reason.

3\. Data Modeling Prompts

Prompt: Canonical entity design prompt  
Design vendor-neutral canonical data entities for a warehouse optimization platform that integrates ERPNext and forklift telemetry.

Include entities for:  
\- product/SKU  
\- warehouse  
\- storage location  
\- sales order  
\- sales order line  
\- stock movement  
\- inventory balance  
\- telemetry point  
\- device state event  
\- demand snapshot  
\- optimization run  
\- recommendation

For each entity provide:  
\- purpose  
\- required fields  
\- optional fields  
\- likely foreign-key relationships

Prompt: CSV schema interpretation prompt  
Given these telemetry CSV schemas:  
\- \<device\_id\>.csv for position/orientation/uncertainty  
\- \<device\_id\>\_STATE.csv for readiness and BLE beacon state

Task:  
Define:  
1\. parsing rules  
2\. validation rules  
3\. bad-data filters  
4\. derived metrics  
5\. how these records should be mapped into analytics-ready internal models

Be explicit about uncertainty thresholds and timestamp handling.

4\. ERPNext Integration Prompts

Prompt: ERPNext integration mapping prompt  
You are integrating ERPNext into a warehouse optimization platform.

Task:  
Identify the minimum ERPNext data domains required to support demand-aware warehouse optimization.

For each domain, provide:  
\- why it matters  
\- likely ERPNext object/doctypes involved  
\- fields we should normalize internally  
\- priority level: must-have, should-have, nice-to-have

Focus on:  
\- items/products  
\- warehouses  
\- sales orders  
\- sales order lines  
\- inventory balances  
\- stock movement / stock ledger concepts

Prompt: ERPNext adapter design prompt  
Design a Python adapter for ERPNext that feeds a warehouse optimization system.

Requirements:  
\- internal models must remain vendor-neutral  
\- adapter should normalize ERPNext responses  
\- design should support fixture-based testing before live integration

Output:  
1\. adapter responsibilities  
2\. method list  
3\. normalization strategy  
4\. error handling strategy  
5\. test strategy

5\. Telemetry and Operational Analysis Prompts

Prompt: Forklift telemetry analysis prompt  
You are analyzing forklift telemetry for warehouse optimization.

Input data includes:  
\- 1 Hz forklift trajectories with x, y, z and quaternion orientation  
\- uncertainty fields std\_x, std\_y, std\_z, std\_R, std\_P, std\_Y  
\- state records with readiness and BLE beacon observations for load and driver identifiers

Task:  
Describe how to transform this data into useful operational signals.

Include:  
1\. quality filtering  
2\. stop/move detection  
3\. route reconstruction  
4\. hotspot detection  
5\. congestion inference  
6\. driver/load association opportunities  
7\. limitations and false-positive risks

Output format:  
Use sections and bullet lists.

Prompt: Demand-to-telemetry linkage prompt  
Design a method for linking ERPNext demand signals and forklift telemetry without overclaiming precision.

Need to cover:  
\- time-window joins  
\- warehouse-level joins  
\- SKU-demand aggregation  
\- zone-level approximation strategies  
\- what can be inferred safely vs what would be speculative

Output format:  
Use two sections:  
\- reliable joins  
\- speculative joins requiring caution

6\. Optimization Prompts

Prompt: Heuristics-first optimization prompt  
You are designing the first optimization engine for a warehouse optimization product.

Constraints:  
\- do not start with reinforcement learning  
\- use available telemetry and ERPNext demand data  
\- prioritize practical recommendations that clients can understand

Task:  
Propose a heuristics-first optimization strategy.

Must include:  
1\. optimization goals  
2\. candidate heuristic methods  
3\. scoring criteria  
4\. required data inputs  
5\. expected outputs  
6\. what would justify later introduction of RL

Prompt: Recommendation generation prompt  
Given telemetry summaries, demand trends, and warehouse movement patterns, generate warehouse optimization recommendations.

Rules:  
\- recommendations must be practical  
\- separate evidence from interpretation  
\- do not invent precision beyond the available data  
\- rank recommendations by expected operational impact and confidence

Output format for each recommendation:  
\- title  
\- recommendation type  
\- observed evidence  
\- likely operational issue  
\- recommended change  
\- expected benefit  
\- confidence  
\- required validation steps

7\. KPI and BI Prompts

Prompt: KPI design prompt  
Design a KPI set for a warehouse optimization platform that combines sales demand and operational telemetry.

Include KPIs for:  
\- throughput  
\- travel intensity  
\- congestion risk  
\- demand concentration  
\- route efficiency  
\- recommendation impact tracking

For each KPI provide:  
\- definition  
\- formula or calculation logic  
\- required inputs  
\- interpretation guidance  
\- likely dashboard placement

Prompt: Power BI handoff prompt  
Design the data outputs required for a Power BI dashboard for warehouse optimization.

Need:  
\- fact tables  
\- dimension tables  
\- refresh expectations  
\- key dashboard views  
\- minimum viable visuals

Keep it implementation-oriented.

8\. Engineering Execution Prompts

Prompt: Repo task planner prompt  
Given the current system architecture and MVP scope, break the work into an implementation plan for a Python repository.

Output:  
\- epics  
\- tasks under each epic  
\- dependencies  
\- suggested order of execution  
\- what can be mocked first  
\- what should not be built yet

Prompt: Code generation guardrail prompt  
You are implementing code for a warehouse optimization system.

Rules:  
\- prefer simple, readable Python  
\- keep domain models explicit  
\- do not introduce heavy dependencies unless justified  
\- optimize for testability  
\- separate vendor-specific logic from core business logic  
\- write code that supports fixture-driven development before live system integration

Before producing code, list:  
1\. assumptions  
2\. module boundaries  
3\. data contracts  
Then provide the code.

9\. Research Prompts

Prompt: WMS evaluation prompt  
Evaluate a WMS for use in a demand-aware warehouse optimization system.

Assess:  
\- warehouse operational coverage  
\- sales/order data availability  
\- API/integration practicality  
\- self-hosting feasibility  
\- ecosystem maturity  
\- fit for MVP

Output format:  
Score each area from 1 to 5 and provide a final recommendation.

Prompt: Methodology comparison prompt  
Compare three approaches for the first warehouse optimization engine:  
1\. heuristic scoring  
2\. simulation-based search  
3\. reinforcement learning

For each approach provide:  
\- implementation difficulty  
\- data requirements  
\- explainability  
\- expected client trust  
\- fit for MVP  
\- fit for later stages

End with a recommendation.

10\. Prompt Usage Guidance  
\- Use architecture prompts before writing core modules.  
\- Use data-model prompts before adding adapters.  
\- Use ERPNext prompts before live integration work.  
\- Use telemetry prompts before designing route/congestion metrics.  
\- Use optimization prompts before claiming intelligent recommendations.  
\- Use KPI prompts before building Power BI outputs.  
\- Use task-planning prompts when converting specs into repository work.

11\. Recommended Prompting Strategy for This Project  
Best order of use:  
1\. product framing  
2\. architecture  
3\. canonical data modeling  
4\. ERPNext mapping  
5\. telemetry interpretation  
6\. heuristics-first optimization design  
7\. KPI/BI design  
8\. task planning  
9\. code generation with guardrails

12\. Key Prompting Principle  
The most important rule for this project is:  
Do not ask the model to jump directly from raw data to grand recommendations.

Instead, prompt in layers:  
\- raw data interpretation  
\- derived signals  
\- operational patterns  
\- optimization candidates  
\- recommendations with confidence and validation needs

That is the safest and most credible way to build this system.  
