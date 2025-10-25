import asyncio
import sys
from pathlib import Path


from autogen_agentchat.ui import Console
from agent.ReportAgent import ReportAgent, ReportResponse
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import StructuredMessage

async def test_team_execution():
    """Test Report Agent with team execution using RoundRobinGroupChat."""
    print("\n" + "=" * 80)
    print("Testing Team Execution")
    print("=" * 80)
    
    # Create the profiling agent
    report_agent = ReportAgent().get_agent()
    
    # Define the profiling task
    task_str = """
    Generate a professional HTML report for the following data quality analysis:

        Goal: Analyze missing values in the RIDEBOOKING table and assess data quality

        Executive Summary:
        Investigation of the RIDEBOOKING table (150,000 rows) found two primary, high-impact issues and several secondary issues. The highest-impact problem is that BOOKING_VALUE and RIDE_DISTANCE contain the literal string 'null' (48,000 occurrences each, ≈32% of rows) instead of SQL NULL or numeric types, which prevents numeric aggregation and analysis until normalized. A secondary issue is duplicate BOOKING_ID values (1,224 duplicate groups, 2,457 rows in duplicate groups, duplicate rate ≈1.64%). TRY_CAST profiling (100k-row sample) indicates non-'null' raw values are generally convertible to numeric and no widespread negative/zero numeric values were observed. Several completeness and cross-field checks failed to run end-to-end due to SQL compilation/type-cast issues (TRY_CAST on native DATE/TIME and inconsistent UNION branch types) in the investigation scripts; however partial runs and samples revealed cross-field contradictions (e.g., Booking Status='Completed' while cancellation/incomplete flags are populated) and many cancelled/no-driver sample rows correlate with BOOKING_VALUE='null'. The pattern of findings suggests ingestion/ETL validation and schema-enforcement gaps. Recommend immediate normalization of literal 'null' text, enforce schema at ingest, implement deduplication rules, fix the failing completeness/cross-field checks, and re-run profiling and monitoring.

        Identified Issues:
        1. [High] Missing values stored as literal string 'null' in numeric fields
        BOOKING_VALUE and RIDE_DISTANCE each contain 48,000 occurrences of the literal string 'null' and show 0 SQL NULLs in the numeric integrity checks. This is ~32% of rows per column and prevents numeric aggregation without normalization. TRY_CAST profiling shows conversion_failures = 0 for other values, indicating other raw strings are numeric.

        2. [Medium] Duplicate BOOKING_ID values
        total_rows = 150,000; duplicate_groups = 1,224 distinct BOOKING_IDs appearing >1; duplicate_records = 2,457 rows in duplicate groups; duplicate_extra_records = 1,233 (rows beyond the first per duplicate group). Duplicate-rate ≈ 1.64%.

        3. [Medium] Schema / type-cast problems in completeness queries (DATE/TIME casting and UNION branch mismatches)
        Completeness-sweep attempts failed to compile because TRY_CAST was applied to native DATE/TIME types (causing 'TRY_CAST cannot be used with DATE->VARCHAR' errors) and some UNION branches returned inconsistent column types/arity, preventing a single-run column-level completeness inventory.

        4. [Medium] Cross-field inconsistencies (Booking Status vs cancellation flags; payment vs missing booking value)
        Although combined cross-field queries failed end-to-end due to SQL errors, partial checks and samples show rows where Booking Status contains 'Completed' while cancellation/incomplete flags are populated and many canceled/no-driver sample rows have BOOKING_VALUE raw = 'null'. Exact counts require focused re-runs.

        5. [High] Ingestion/ETL validation gaps and lack of enforced schema
        The combination of large literal 'null' text in numeric fields, varchar storage of numeric data, duplicate keys, and contradictory cross-field values suggests weak or missing ingestion validation and schema enforcement (data contract). This increases downstream risk for analytics and billing.

        Recommendations:
        1. Immediate normalization: convert literal 'null' strings to SQL NULL for BOOKING_VALUE and RIDE_DISTANCE (and any other columns with 'null' text) as an urgent ETL patch. After normalization, persist or expose BOOKING_VALUE and RIDE_DISTANCE as numeric types (DECIMAL) in the curated layer.
        2. Enforce schema and data-contract at ingest: add type checks and null-semantics validation to ingestion jobs. Route malformed rows to a quarantine table/topic with reason metadata and alerting instead of silently storing bad values.
        3. Implement deduplication rules: define a business rule (e.g., keep latest by DATE+TIME, prefer 'Completed' status, or first-seen) and dedupe during ETL or via a deduped view. Track source/retry IDs upstream to prevent reoccurrence.
        4. Fix completeness and cross-field checks: re-run per-column completeness queries using TO_VARCHAR/TO_CHAR for DATE/TIME when checking literal text and TRY_CAST only on VARCHAR numeric fields. Avoid mixing heterogeneous casts in large UNIONs — run focused COUNT() and SAMPLE (LIMIT 5–10) queries per rule.
        5. Decide backfill policy for historical BOOKING_VALUE on cancelled/no-driver rides (NULL vs 0) and apply documented backfill if required for downstream consumers.
        6. Create a short-term curated view exposing normalized numeric columns so analytics can resume, for example: BOOKING_VALUE_NUM = TRY_CAST(NULLIF(LOWER(TRIM(BOOKING_VALUE)),'null') AS DECIMAL(18,4)).
        7. Add data-quality monitoring and automated tests (daily jobs and CI checks) for: percent literal-'null' by column, conversion_failures, duplicate-rate, and cross-field contradiction counts; alert when thresholds are breached.


        Investigation Details:
        Total queries executed: 16 across 4 tasks
        Total profiles generated: 1 across 1 tasks

        Profiling Reports Available:
        - HTML: RIDEBOOKING_profile_20251016_083617.html
        - JSON: RIDEBOOKING_profile_20251016_083621.json


        Please generate a comprehensive, well-formatted HTML report with all sections.
        End your response with REPORT_COMPLETE when finished.
    """
    
    termination = MaxMessageTermination(max_messages=5)
    team = RoundRobinGroupChat(
        [report_agent],
        termination_condition=termination,
        custom_message_types=[StructuredMessage[ReportResponse]]
    )
    
    # Run with console output
    result = await Console(team.run_stream(task=task_str))

    # Extract report
    for message in reversed(result.messages):
        if hasattr(message, 'content') and isinstance(message.content, ReportResponse):
            html_report = message.content.html
            if html_report:
                # Save HTML report to file
                goal = "Analyze missing values in RIDEBOOKING table"
                report_path = save_html_report(html_report, goal)
                print(f"✅ Report generated and saved to: {report_path}")
    
    print("\n" + "=" * 80)
    print("Team execution completed!")
    print("=" * 80)
    print(report_path)

def save_html_report(html: str, goal: str) -> str:
    """Save HTML report to file."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create safe filename from goal
    safe_goal = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in goal)
    safe_goal = safe_goal[:50]  # Limit length
    filename = f"data_quality_report_{safe_goal}_{timestamp}.html"
    
    # Create reports directory if it doesn't exist
    reports_dir = Path("ge_reports")
    reports_dir.mkdir(exist_ok=True)
    report_path = reports_dir / filename
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(report_path)

if __name__ == "__main__":

    async def main() -> None:
        await test_team_execution()

    asyncio.run(main())